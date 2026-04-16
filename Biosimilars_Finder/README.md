# Biosimilars Finder
#### Description:

Query FDA open API database as well as the most recent csv file posted on FDA's
Purple book website for available biologics and biosimilars information

Class Drug is used to store particular information of a drug and available biosimilars info"

get_brand() queries the FDA API for the openfda data associated with a drug and store info into the drug instance

As the FDA API doesn't take RE query or provide detailed functionalities for drug brand name check, rf"^{name}(?![\w-])" is used to do a second round check if a drug is a valid drug given the FDA database. This helps to filter out cases like "name-xxxx" or "XX name" or "xxxnamexxx"

    Parameters:
        drug (Class Drug): Drug class instance that is used to store FDA query results
        name (str): User input drug name to be checked with FDA database

    Raises:
        KeyError: If a drug's brand name exist FDA's database but info such as generic/molecule name, route, or moa is not available (e.g. Humira)
        ValueError : if the FDA API cannot be accessed

get_biologics () finds the most recent PurpleBook CSV file and identify if a drug is biologics and if it has biosimilar. Retrieve biosimilars info and store in the Drug class instance if available"

It automatically checks 24 months starting from the current month to find the most recent Purple Book csv. The function should be called only after get_brand () is called.

It determines if a drug is biologics based on PurpleBook's cvs field - Proprietary Name.

It determines if a drug is biologics based on PurpleBook's cvs field - Ref. Product Proprietary Name

Class Drug property self._biosimilars stores all fields of the FDA PurpleBook csv file of a drug's biosimilars as Pandas DataFrame, not just the ones that prn_biosim() prints

    Parameters:
        drug (Class Drug): Drug class instance that is used to store FDA query results
        name (str): User input drug name to be checked with the PurpleBook csv fil


prn_biosim() print a Drug instance's selected biosimilars information. Class Drug property self._biosimilars stores all fields of the FDA PurpleBook csv file of a drug's biosimilars as Pandas DataFrame, not just the ones that prn_biosim() prints so more info can be easily added to the output table if needed

    Parameters:
        drug (Class Drug): Drug class instance that is used to store FDA query results

    ValueError : if the drug is not biologics or if it doesn't have biosimilars info



TODO
1. The three key functions - get_brand(), get_biologics(), prn_biosim() can be easily changed to instance method as they were designed as method for the class Drug
2. One can sometime access a PurpleBook CSV when it is not even officially posted on FDA's PurpleBook website. For example, in March, 2026. The most updated file should be February, 2026 based on PurpleBook's website but March, 2026 csv can already be accessed. This may/may not be the intended behavior of the program
3. The reason that the program has to automatically download the PurpleBook csv, hold it in memory for query etc is because FDA doesn't currently have an API for PurpleBook. It would be great to change the PurpleBook query to an APL query once an API is available
