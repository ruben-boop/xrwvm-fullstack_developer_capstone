from .models import Dealer

def initiate_dealers():
    """Populate the database with sample dealer data"""
    dealer_data = [
        {
            "full_name": "Acme Motors",
            "city": "New York",
            "state": "NY",
            "address": "123 Main Street",
            "zip": "10001",
        },
        {
            "full_name": "Bob's Auto Sales",
            "city": "Los Angeles",
            "state": "CA",
            "address": "456 Sunset Boulevard",
            "zip": "90001",
        },
        {
            "full_name": "Charlie's Car Emporium",
            "city": "Chicago",
            "state": "IL",
            "address": "789 Michigan Avenue",
            "zip": "60601",
        },
        {
            "full_name": "Dave's Dealership",
            "city": "Houston",
            "state": "TX",
            "address": "321 Main Street",
            "zip": "77001",
        },
        {
            "full_name": "Eva's Elite Motors",
            "city": "Phoenix",
            "state": "AZ",
            "address": "654 Central Avenue",
            "zip": "85001",
        },
        {
            "full_name": "Frank's Fine Autos",
            "city": "Philadelphia",
            "state": "PA",
            "address": "987 Market Street",
            "zip": "19103",
        },
        {
            "full_name": "Grace's Cars & Trucks",
            "city": "San Antonio",
            "state": "TX",
            "address": "159 Broadway",
            "zip": "78201",
        },
        {
            "full_name": "Henry's Auto Haven",
            "city": "San Diego",
            "state": "CA",
            "address": "753 Pacific Beach Boulevard",
            "zip": "92109",
        },
    ]

    for data in dealer_data:
        # Check if dealer already exists to avoid duplicates
        if not Dealer.objects.filter(full_name=data["full_name"]).exists():
            Dealer.objects.create(
                full_name=data["full_name"],
                city=data["city"],
                state=data["state"],
                address=data["address"],
                zip=data["zip"],
            )
