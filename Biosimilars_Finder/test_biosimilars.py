import pytest
import pandas as pnds
from biosimilars import Drug, get_brand, get_biologics, prn_biosim


def test_init () :
    drug = Drug ("remicade")
    assert drug.brand_name == "remicade"
    assert drug.is_drug == False
    assert drug.is_biologics == False
    assert drug.has_biosimilar == False
    with pytest.raises(TypeError) :
        jar= Drug ("remicade", "rituximab")


def test_get_brand () :
    drug = Drug ()
    get_brand (drug, "rituxan")
    assert drug.is_drug == True
    assert drug._generic_name == "Rituximab and hyaluronidase"

    drug = Drug ()
    get_brand (drug, "remicade")
    assert drug.is_drug == True

    drug = Drug ()
    get_brand (drug, "HumiRa")
    assert drug.is_drug == True

    drug = Drug ()
    get_brand (drug, "KeyTruda")
    assert drug.is_drug == True

    drug = Drug ()
    get_brand (drug, "r")
    assert drug.is_drug == False

    drug = Drug ()
    get_brand (drug, "re")
    assert drug.is_drug == False

    drug = Drug ()
    get_brand (drug, "Not a Drug")
    assert drug.is_drug == False

    drug = Drug ()
    get_brand (drug, "")
    assert drug.is_drug == False

    with pytest.raises(TypeError) :
       get_brand (drug)
    with pytest.raises(TypeError) :
       get_brand (drug,"xxx","XXX")


def test_get_biologics () :
    drug = Drug ()
    get_brand (drug, "rituxan")
    get_biologics (drug, "rituxan")
    assert drug.is_biologics == True
    assert drug.has_biosimilar == True

    drug = Drug ()
    get_brand (drug, "HuMira")
    get_biologics (drug, "Humira")
    assert drug.is_biologics == True
    assert drug.has_biosimilar == True
    assert isinstance(drug._biosimilars, pnds.DataFrame)

    drug = Drug ()
    get_brand (drug,"Remicade")
    get_biologics (drug,"reMIcade")
    assert drug.is_biologics == True
    assert drug.has_biosimilar == True
    assert isinstance(drug._biosimilars, pnds.DataFrame)

    drug = Drug ()
    get_brand (drug,"KeyTruda")
    get_biologics (drug, "keytruda")
    assert drug.is_biologics == True
    assert drug.has_biosimilar == False
    assert not isinstance(drug._biosimilars, pnds.DataFrame)

    drug = Drug ()
    get_brand (drug, "lipitor")
    get_biologics (drug, "lipitor")
    assert drug.is_biologics == False
    assert drug.has_biosimilar == False
    assert not isinstance(drug._biosimilars, pnds.DataFrame)

    with pytest.raises(TypeError) :
       get_biologics (drug)
    with pytest.raises(TypeError) :
       get_biologics (drug,"xxx","XXX")

def test_prn_biosim() :
    with pytest.raises(TypeError) :
        prn_biosim()
    drug = Drug ()
    get_brand (drug, "lipitor")
    get_biologics (drug, "lipitor")
    with pytest.raises(ValueError) :
        prn_biosim(drug)
