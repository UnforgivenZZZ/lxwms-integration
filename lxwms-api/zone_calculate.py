from pyzipcode import ZipCodeDatabase
import geopy.distance

def estimate_zone(origin, destination):
    zcdb = ZipCodeDatabase()
    try:
        orig_zip = zcdb[origin]
        dest_zip = zcdb[destination]
    except:
        return None
    
    # Calculate distance
    orig_coords = (orig_zip.latitude, orig_zip.longitude)
    dest_coords = (dest_zip.latitude, dest_zip.longitude)
    distance = geopy.distance.distance(orig_coords, dest_coords).miles
    
    # Map distance to USPS-like zones (approximate)
    if distance <= 50:
        return 1
    elif distance <= 150:
        return 2
    elif distance <= 300:
        return 3
    elif distance <= 600:
        return 4
    elif distance <= 1000:
        return 5
    elif distance <= 1400:
        return 6
    elif distance <= 1800:
        return 7
    else:
        return 8

# Example
print(estimate_zone('94536', '94538'))  # Output: ~8

for i in range(94536, 100000):
    print(i, estimate_zone('94536', str(i).zfill(5)))