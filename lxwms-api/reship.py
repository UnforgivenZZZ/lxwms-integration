import requests 
import lxwms_utils
trackings = []
track = input('track: ')
while track != str(-1):
    trackings.append(str(track))
    track = input('track: ')
for track in trackings:
    job = lxwms_utils.get_job_by_track(track)
    data = lxwms_utils.get_label_by_job(job)
    # print(data)
    while True:
        try:
            lxwms_utils.download_and_save_file(data, 'reship-sf')
            break
        except:
            continue
