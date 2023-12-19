from cerberus import Validator
import redfin
import pytest
import pprint

redfin.BASE_CONFIG["cache"] = True

pp = pprint.PrettyPrinter(indent=4)


def validate_or_fail(item, validator):
    if not validator.validate(item):
        pp.pformat(item)
        pytest.fail(
            f"Validation failed for item: {pp.pformat(item)}\nErrors: {validator.errors}"
        )


property_sale_schema = {
    "schema": {
        "type": "dict",
        "schema": {
            "address": {"type": "string"},
            "description": {"type": "string"},
            "price": {"type": "string"},
            "estimatedMonthlyPrice": {"type": "string"},
            "propertyUrl": {"type": "string"},
            "attachments": {"type": "list", "schema": {"type": "string"}},
            "details": {"type": "list", "schema": {"type": "string"}},
            "features": {
                "type": "dict",
                "schema": {
                    "Parking Information": {
                        "type": "list",
                        "schema": {"type": "string"},
                    }
                },
            },
        },
    }
}

property_rent_schema = {
    "schema": {
        "type": "dict",
        "schema": {
            "rentalId": {"type": "string"},
            "unitTypesByBedroom": {
                "type": "list",
                "schema": {
                    "type": "dict",
                    "schema": {
                        "bedroomTitle": {"type": "string"},
                        "availableUnitTypes": {
                            "type": "list",
                            "schema": {
                                "type": "dict",
                                "schema": {
                                    "unitTypeId": {"type": "string"},
                                    "units": {
                                        "type": "list",
                                        "schema": {
                                            "type": "dict",
                                            "schema": {
                                                "unitId": {"type": "string"},
                                                "bedrooms": {"type": "integer"},
                                                "depositCurrency": {"type": "string"},
                                                "fullBaths": {"type": "integer"},
                                                "halfBaths": {"type": "integer"},
                                                "name": {"type": "string"},
                                                "rentCurrency": {"type": "string"},
                                                "rentPrice": {"type": "integer"},
                                                "sqft": {"type": "string"},
                                                "status": {"type": "string"},
                                            },
                                        },
                                    },
                                    "availableUnits": {"type": "integer"},
                                    "bedrooms": {"type": "integer"},
                                    "fullBaths": {"type": "integer"},
                                    "halfBaths": {"type": "integer"},
                                    "name": {"type": "string"},
                                    "rentPriceMax": {"type": "integer"},
                                    "rentPriceMin": {"type": "integer"},
                                    "sqftMax": {"type": "integer"},
                                    "sqftMin": {"type": "integer"},
                                    "status": {"type": "string"},
                                    "style": {"type": "string"},
                                    "totalUnits": {"type": "integer"},
                                },
                            },
                        },
                    },
                },
            },
        },
    }
}

search_schema = {
    "schema": {
        "type": "dict",
        "schema": {
            "mlsId": {
                "type": "dict",
                "schema": {
                    "label": {"type": "string"},
                    "value": {"type": "string"},
                },
            },
            "price": {
                "type": "dict",
                "schema": {
                    "value": {"type": "integer"},
                    "level": {"type": "integer"},
                },
            },
            "beds": {"type": "integer"},
            "baths": {"type": "integer"},
            "fullBaths": {"type": "integer"},
            "location": {
                "type": "dict",
                "schema": {
                    "value": {"type": "string"},
                    "level": {"type": "integer"},
                },
            },
            "streetLine": {
                "type": "dict",
                "schema": {
                    "value": {"type": "string"},
                    "level": {"type": "integer"},
                },
            },
            "countryCode": {"type": "string"},
            "showAddressOnMap": {"type": "boolean"},
            "soldDate": {"type": "integer"},
            "searchStatus": {"type": "integer"},
            "propertyType": {"type": "integer"},
            "uiPropertyType": {"type": "integer"},
            "listingType": {"type": "integer"},
            "propertyId": {"type": "integer"},
            "listingId": {"type": "integer"},
            "dataSourceId": {"type": "integer"},
            "marketId": {"type": "integer"},
        },
    }
}


@pytest.mark.asyncio
async def test_properties_for_sale_scraping():
    properties_sale_data = await redfin.scrape_property_for_sale(
        urls=[
            "https://www.redfin.com/WA/Seattle/506-E-Howell-St-98122/unit-W303/home/46456",
            "https://www.redfin.com/WA/Seattle/1105-Spring-St-98104/unit-405/home/12305595",
        ]
    )
    validator = Validator(property_sale_schema, allow_unknown=True)
    for item in properties_sale_data:
        validate_or_fail(item, validator)
    assert len(properties_sale_data) >= 1


@pytest.mark.asyncio
async def test_properties_for_rent_scraping():
    properties_rent_data = await redfin.scrape_property_for_rent(
        urls=[
            "https://www.redfin.com/WA/Seattle/Onni-South-Lake-Union/apartment/147020546",
            "https://www.redfin.com/WA/Seattle/The-Ivey-on-Boren/apartment/146904423",
        ]
    )
    validator = Validator(property_rent_schema, allow_unknown=True)
    for item in properties_rent_data:
        validate_or_fail(item, validator)
    assert len(properties_rent_data) >= 1


@pytest.mark.asyncio
async def test_search_scraping():
    search_data = await redfin.scrape_search(
        url="https://www.redfin.com/stingray/api/gis?al=1&include_nearby_homes=true&market=seattle&num_homes=350&ord=redfin-recommended-asc&page_number=1&poly=-122.54472%2047.44109%2C-122.11144%2047.44109%2C-122.11144%2047.78363%2C-122.54472%2047.78363%2C-122.54472%2047.44109&sf=1,2,3,5,6,7&start=0&status=1&uipt=1,2,3,4,5,6,7,8&user_poly=-122.278298%2047.739783%2C-122.278985%2047.739783%2C-122.279671%2047.739783%2C-122.325677%2047.743015%2C-122.330483%2047.743015%2C-122.335290%2047.743015%2C-122.346276%2047.742554%2C-122.351769%2047.742092%2C-122.357262%2047.741168%2C-122.362756%2047.740245%2C-122.368249%2047.739321%2C-122.373742%2047.737936%2C-122.378548%2047.736551%2C-122.383355%2047.735165%2C-122.388161%2047.733780%2C-122.392968%2047.732856%2C-122.397088%2047.731471%2C-122.401208%2047.730085%2C-122.404641%2047.728238%2C-122.407388%2047.726390%2C-122.410134%2047.724081%2C-122.412194%2047.721771%2C-122.414254%2047.718999%2C-122.416314%2047.716228%2C-122.418374%2047.712532%2C-122.421120%2047.708835%2C-122.423867%2047.704677%2C-122.426614%2047.700056%2C-122.429360%2047.695434%2C-122.432107%2047.690813%2C-122.434853%2047.686190%2C-122.437600%2047.681568%2C-122.439660%2047.676945%2C-122.441033%2047.671859%2C-122.442406%2047.666310%2C-122.444466%2047.660298%2C-122.446526%2047.653823%2C-122.447900%2047.646885%2C-122.449960%2047.639946%2C-122.451333%2047.632543%2C-122.452020%2047.625139%2C-122.452020%2047.619122%2C-122.452020%2047.613105%2C-122.452020%2047.607087%2C-122.452020%2047.601994%2C-122.452020%2047.596438%2C-122.451333%2047.590881%2C-122.449960%2047.586250%2C-122.448586%2047.581619%2C-122.447213%2047.576987%2C-122.445153%2047.572818%2C-122.443093%2047.568648%2C-122.441033%2047.564942%2C-122.438973%2047.561235%2C-122.436227%2047.557992%2C-122.433480%2047.554748%2C-122.430734%2047.551967%2C-122.428674%2047.549187%2C-122.426614%2047.546869%2C-122.423867%2047.544552%2C-122.421120%2047.541771%2C-122.418374%2047.539453%2C-122.415627%2047.537136%2C-122.412881%2047.534818%2C-122.410134%2047.532500%2C-122.406014%2047.530182%2C-122.401894%2047.527864%2C-122.397775%2047.525545%2C-122.392968%2047.523691%2C-122.388161%2047.521372%2C-122.383355%2047.519517%2C-122.378548%2047.517662%2C-122.373055%2047.515807%2C-122.368249%2047.513952%2C-122.362756%2047.512561%2C-122.357262%2047.511170%2C-122.351769%2047.509314%2C-122.345589%2047.507923%2C-122.339410%2047.506995%2C-122.332543%2047.506068%2C-122.325677%2047.505140%2C-122.318810%2047.504212%2C-122.312630%2047.503285%2C-122.307137%2047.502821%2C-122.302331%2047.502357%2C-122.298211%2047.502357%2C-122.294091%2047.502357%2C-122.289285%2047.502821%2C-122.285165%2047.503748%2C-122.281045%2047.504676%2C-122.276925%2047.505604%2C-122.272805%2047.506532%2C-122.267999%2047.507923%2C-122.263192%2047.508851%2C-122.258385%2047.509314%2C-122.253579%2047.509778%2C-122.248772%2047.510242%2C-122.245339%2047.510242%2C-122.240533%2047.510706%2C-122.237099%2047.511170%2C-122.233666%2047.511633%2C-122.231606%2047.512561%2C-122.229546%2047.513025%2C-122.228173%2047.513952%2C-122.226800%2047.515344%2C-122.226113%2047.517199%2C-122.225426%2047.519517%2C-122.224053%2047.522299%2C-122.222680%2047.526009%2C-122.221993%2047.529718%2C-122.220620%2047.533427%2C-122.219247%2047.537136%2C-122.218560%2047.540844%2C-122.217187%2047.545016%2C-122.216500%2047.549650%2C-122.215127%2047.554748%2C-122.213067%2047.561235%2C-122.212380%2047.568648%2C-122.211694%2047.576524%2C-122.211694%2047.584861%2C-122.211694%2047.593660%2C-122.211694%2047.602920%2C-122.211694%2047.611716%2C-122.211694%2047.620048%2C-122.211694%2047.627452%2C-122.211694%2047.634856%2C-122.211694%2047.641796%2C-122.212380%2047.648735%2C-122.213754%2047.655211%2C-122.215127%2047.661223%2C-122.216500%2047.667235%2C-122.218560%2047.673246%2C-122.220620%2047.679256%2C-122.223367%2047.684341%2C-122.226113%2047.688964%2C-122.228173%2047.692661%2C-122.230233%2047.695897%2C-122.232293%2047.699132%2C-122.235040%2047.701904%2C-122.237099%2047.704677%2C-122.239846%2047.707449%2C-122.242593%2047.710221%2C-122.244653%2047.712994%2C-122.246713%2047.715304%2C-122.248772%2047.717613%2C-122.250832%2047.719923%2C-122.252206%2047.721771%2C-122.253579%2047.723619%2C-122.254952%2047.725004%2C-122.256326%2047.726390%2C-122.257699%2047.727314%2C-122.258385%2047.728238%2C-122.259072%2047.729161%2C-122.259759%2047.730085%2C-122.260445%2047.730547%2C-122.261132%2047.731471%2C-122.261819%2047.731932%2C-122.262505%2047.732394%2C-122.263192%2047.733318%2C-122.263879%2047.733780%2C-122.264565%2047.734242%2C-122.265252%2047.734703%2C-122.265939%2047.735165%2C-122.266625%2047.735627%2C-122.267312%2047.736089%2C-122.267999%2047.736551%2C-122.268685%2047.737012%2C-122.270058%2047.737936%2C-122.270745%2047.738859%2C-122.271432%2047.739783%2C-122.272118%2047.740245%2C-122.272805%2047.740707%2C-122.273492%2047.741168%2C-122.274178%2047.741168%2C-122.274865%2047.741630%2C-122.275552%2047.741630%2C-122.278298%2047.739783&v=8&zoomLevel=11"
    )
    validator = Validator(search_schema, allow_unknown=True)
    for item in search_data:
        validate_or_fail(item, validator)
    assert len(search_data) >= 2
