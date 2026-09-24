import libs


def load_data(participent_id, event_id):
    Annotation_event_ID={
        "Sleep stage W":1,
        "Sleep stage 1":2,
        "Sleep stage 2":2,
        "Sleep stage 3":2,
        "Sleep stage 4":2,
        "Sleep stage R":3
    }
    [participent_file] =libs.data(subjects=[participent_id],recording=[1])
    raw_edf = libs.mne.io.read_raw_edf(
        participent_file[0],
        stim_channel="Event Marker",
        infer_types=True,
        preload=True,
        verbose="error")
    
    annotation_edf=libs.mne.read_annotations(participent_file[1])
    
    annotation_edf.crop(annotation_edf[1]["onset"]-30*240,
                        annotation_edf[-2]["onset"]+30*240)
    
    raw_edf.set_annotations(annotation_edf,emit_warning=False)
    
    events,_=libs.mne.events_from_annotations(
        raw_edf,event_id=Annotation_event_ID,chunk_duration=30.0
    )
    
    
    tmax= 30.0-10.0 /raw_edf.info["sfreq"]
    
    epochs= libs.mne.Epochs(
        raw=raw_edf,
        events=events,
        event_id=event_id,
        tmin=1.0,
        tmax=tmax,
        baseline=None,
        preload=True
    )
    
    return raw_edf,events,epochs
