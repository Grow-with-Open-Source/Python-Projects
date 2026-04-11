import requests
import pandas as pnds
import re
import time
from tabulate import tabulate
from datetime import datetime
from dateutil.relativedelta import relativedelta
from io import StringIO


def main () :

    """
    Query FDA open API database as well as the most recent csv data file on FDA's
    Purple book website for available biologics and biosimilars information

    """

    name= input("Brand Name: ").strip()
    drug=Drug(name)
    get_brand(drug,name)
    if drug.is_drug :
        get_biologics(drug,name)
    print (drug)

    if drug.is_biologics and drug.has_biosimilar:
        biosim= input ("Do you want more biosimilars info?[Y/N] ").lower().strip()
        if biosim == "y" or biosim == "yes" :
            prn_biosim(drug)


class Drug:

    """
    Class Drug is used to store particular information of a drug and available biosimilars info"
    """

    def __init__(self, brand_name=[]):
        self.brand_name=brand_name
        self.is_drug = False
        self._generic_name=""
        self._route=""
        self._moa=""
        self.is_biologics= False
        self.has_biosimilar = False
        self._biosimilars = []

    def __str__(self):
        if not self.is_drug :
            s= f"{self.brand_name} is not a brand drug based on the FDA database"
        else :
            s= f"\nBrand Name: {self.brand_name}\n"
            s += f"Molecule Name: {self._generic_name}\n"
            s += f"Route: {self._route}\n"
            s += f"Mechnism of Action: {self._moa}\n"
            s += "Biologics: Yes\n" if self.is_biologics else "Biologics: N/A\n"
            s += "Biosimilars: Yes" if self.has_biosimilar else "Biosimilars: N/A"
        return s


def get_brand (drug,name):

    """
    Query the FDA API for the openfda data associated with a drug and store info into the drug instance

    Parameters:
        drug (Class Drug): Drug class instance that is used to store FDA query results
        name (str): User input drug name to be checked with FDA database

    Raises:
        KeyError: If a drug's brand name exist FDA's database but info such as generic/molecule
          name, route, or moa is not available (e.g. Humira)
        ValueError : if the FDA API cannot be accessed
    """

    url= f'https://api.fda.gov/drug/label.json?search=openfda.brand_name:"{name}"&limit=1'

    try :
        r = requests.get(url, timeout=10)  
    except requests.exceptions.RequestException as e:
        print("FDA API not avaialble")

    if r.status_code ==200 :
        response = r.json()  
        results = response.get("results", [])
        openfda = results[0].get("openfda",{})

        fda_name = openfda["brand_name"][0].strip().capitalize ()
        pattern=rf"^{name}(?![\w-])"

        if match :=re.search(pattern,fda_name,re.I) :
            drug.brand_name = fda_name.capitalize()
            drug.is_drug=True

            try :
                drug._generic_name=openfda["generic_name"][0].capitalize()
            except KeyError :
                drug._generic_name ="N/A"
            try :
                drug._route=openfda["route"][0].capitalize()
            except KeyError :
                drug._route ="N/A"
            try :
                drug._moa=openfda["pharm_class_moa"][0].capitalize()[:-6] # removing " [moa]" at the end of the return string
            except KeyError :
                drug._moa ="N/A"
        else :
                drug.is_drug=False
    else :
        drug.is_drug=False


def get_biologics (drug,name):

    """
        Finds the most recent PurpleBook CSV file and identify if a drug is biologics
        and if it has biosimilar. Retrieve biosimilars info and store in the Drug class
        instance if available"

        Automatically check 24 months starting from the current month to find the most
        recent Purple Book csv

    Parameters:
        drug (Class Drug): Drug class instance that is used to store FDA query results
        name (str): User input drug name to be checked with the PurpleBook csv file
    """

    now = datetime.now()
    # number of months back from current to search purplebook data
    num_months= 24
    base_url = "https://www.accessdata.fda.gov/drugsatfda_docs/PurpleBook"
    headers = {"user-Agent": "Mozilla/5.0"}

    for i in range (num_months) :
        past = now - relativedelta(months=i)
        month_name = past.strftime("%B").capitalize()
        year=str(past.year)
        filename = f"purplebook-search-{month_name}-data-download.csv"
        url = f"{base_url}/{year}/{filename}"
        pb_read_success = False
 #      
        try:
            r= requests.get(url, headers=headers)
            if r.status_code ==200 :
                pb_read_success = True
                pb = pnds.read_csv(StringIO(r.text), skiprows=3)
                break
            else :
                time.sleep(2)
        except Exception as e:
            time.sleep(2)

    if pb_read_success :
        biologics_matches = pb[pb["Proprietary Name"].str.contains(name, case=False, na=False)]
        drug.is_biologics = not biologics_matches.empty

        if drug.is_biologics :
            biosimilars_matches = pb[pb["Ref. Product Proprietary Name"].str.contains(name, case=False, na=False)]
            drug.has_biosimilar = not biosimilars_matches.empty
            if drug.has_biosimilar :
                    drug._biosimilars=biosimilars_matches


def prn_biosim(drug) :

    """
    Print a Drug instance's selected biosimilars information

    Parameters:
        drug (Class Drug): Drug class instance that is used to store FDA query results

    ValueError : if the drug is not biologics or if it doesn't have biosimilars info

    """

    if drug.has_biosimilar == True and drug.is_biologics == True :
        print(tabulate(
            drug._biosimilars[['Proprietary Name','Proper Name','Strength','Applicant','Approval Date']],
            headers=['Brand Name','Molecule Name','Strength','Applicant','Approval Date'],
            tablefmt="grid",
            showindex=False,
            maxcolwidths=[None,None,None,15,None]
        ))
    else :
        raise ValueError ("The drug does not have biosimlar")


if __name__ == "__main__" :
    main ()

