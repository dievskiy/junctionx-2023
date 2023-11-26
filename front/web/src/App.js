import logo from './logo.svg';
import './App.css';

import {Calendar, momentLocalizer} from 'react-big-calendar'
import 'react-big-calendar/lib/css/react-big-calendar.css'
// import 'react-big-calendar/lib/addons/dragAndDrop/styles';
import 'react-big-calendar/lib/addons/dragAndDrop/styles.css';
import moment from 'moment'
import withDragAndDrop from 'react-big-calendar/lib/addons/dragAndDrop'
import 'react-big-calendar/lib/addons/dragAndDrop/styles.css'
import {useEffect, useState} from "react";

const DnDCalendar = withDragAndDrop(Calendar)

const localizer = momentLocalizer(moment)

// enum for machines
const machines = {
    TB1: 1,
    TB2: 2,
    VB1: 3,
    VB2: 4,
    U: 5,
}

const myEventsList = [
    {
        id: 0,
        title: 'TB1',
        allDay: false,
        start: new Date(2023, 10, 25, 18, 40),
        end: new Date(2023, 10, 25, 19, 20),
        resourceId: 1,
        machine: machines.TB1,
    },
    {
        id: 1,
        title: 'TB2',
        allDay: false,
        start: new Date(2023, 10, 25, 14, 0),
        end: new Date(2023, 10, 25, 14, 50),
        resourceId: 2,
        machine: machines.TB2,
    },
    {
        id: 2,
        title: 'VB1',
        allDay: false,
        start: new Date(2023, 10, 25, 11, 15),
        end: new Date(2023, 10, 25, 11, 45),
        resourceId: 3,
        machine: machines.VB1,
    },
];
// seems like there's no overlap support with resources

function App() {
    const eventss = [{"title": "VB2", "machine": "VB2", "start": 324, "end": 336, "patient": 0, "region": "Lung_special"}, {"title": "VB1", "machine": "VB1", "start": 348, "end": 360, "patient": 0, "region": "Lung_special"}, {"title": "VB2", "machine": "VB2", "start": 396, "end": 408, "patient": 0, "region": "Lung_special"}, {"title": "U", "machine": "U", "start": 108, "end": 120, "patient": 1, "region": "Breast"}, {"title": "U", "machine": "U", "start": 120, "end": 132, "patient": 1, "region": "Breast"}, {"title": "U", "machine": "U", "start": 132, "end": 144, "patient": 1, "region": "Breast"}, {"title": "U", "machine": "U", "start": 144, "end": 156, "patient": 1, "region": "Breast"}, {"title": "VB2", "machine": "VB2", "start": 156, "end": 168, "patient": 1, "region": "Breast"}, {"title": "VB2", "machine": "VB2", "start": 168, "end": 180, "patient": 1, "region": "Breast"}, {"title": "VB2", "machine": "VB2", "start": 180, "end": 192, "patient": 1, "region": "Breast"}, {"title": "VB1", "machine": "VB1", "start": 192, "end": 204, "patient": 1, "region": "Breast"}, {"title": "VB1", "machine": "VB1", "start": 204, "end": 216, "patient": 1, "region": "Breast"}, {"title": "VB2", "machine": "VB2", "start": 216, "end": 228, "patient": 1, "region": "Breast"}, {"title": "U", "machine": "U", "start": 228, "end": 240, "patient": 1, "region": "Breast"}, {"title": "VB2", "machine": "VB2", "start": 240, "end": 252, "patient": 1, "region": "Breast"}, {"title": "VB1", "machine": "VB1", "start": 252, "end": 264, "patient": 1, "region": "Breast"}, {"title": "U", "machine": "U", "start": 264, "end": 276, "patient": 1, "region": "Breast"}, {"title": "U", "machine": "U", "start": 276, "end": 288, "patient": 1, "region": "Breast"}, {"title": "VB2", "machine": "VB2", "start": 288, "end": 300, "patient": 1, "region": "Breast"}, {"title": "U", "machine": "U", "start": 300, "end": 312, "patient": 1, "region": "Breast"}, {"title": "U", "machine": "U", "start": 312, "end": 324, "patient": 1, "region": "Breast"}, {"title": "VB1", "machine": "VB1", "start": 324, "end": 336, "patient": 1, "region": "Breast"}, {"title": "VB2", "machine": "VB2", "start": 336, "end": 348, "patient": 1, "region": "Breast"}, {"title": "VB2", "machine": "VB2", "start": 348, "end": 360, "patient": 1, "region": "Breast"}, {"title": "VB2", "machine": "VB2", "start": 360, "end": 372, "patient": 1, "region": "Breast"}, {"title": "U", "machine": "U", "start": 372, "end": 384, "patient": 1, "region": "Breast"}, {"title": "VB1", "machine": "VB1", "start": 384, "end": 396, "patient": 1, "region": "Breast"}, {"title": "VB1", "machine": "VB1", "start": 396, "end": 408, "patient": 1, "region": "Breast"}, {"title": "VB2", "machine": "VB2", "start": 408, "end": 420, "patient": 1, "region": "Breast"}, {"title": "VB1", "machine": "VB1", "start": 420, "end": 432, "patient": 1, "region": "Breast"}, {"title": "U", "machine": "U", "start": 432, "end": 444, "patient": 1, "region": "Breast"}, {"title": "U", "machine": "U", "start": 444, "end": 456, "patient": 1, "region": "Breast"}, {"title": "VB1", "machine": "VB1", "start": 456, "end": 468, "patient": 1, "region": "Breast"}, {"title": "VB2", "machine": "VB2", "start": 60, "end": 72, "patient": 2, "region": "Abdomen"}, {"title": "VB2", "machine": "VB2", "start": 96, "end": 108, "patient": 2, "region": "Abdomen"}, {"title": "VB1", "machine": "VB1", "start": 288, "end": 300, "patient": 2, "region": "Abdomen"}, {"title": "VB1", "machine": "VB1", "start": 12, "end": 24, "patient": 3, "region": "Lung"}, {"title": "VB2", "machine": "VB2", "start": 24, "end": 36, "patient": 3, "region": "Lung"}, {"title": "VB1", "machine": "VB1", "start": 36, "end": 48, "patient": 3, "region": "Lung"}, {"title": "VB1", "machine": "VB1", "start": 108, "end": 120, "patient": 3, "region": "Lung"}, {"title": "VB1", "machine": "VB1", "start": 120, "end": 132, "patient": 3, "region": "Lung"}, {"title": "VB2", "machine": "VB2", "start": 132, "end": 144, "patient": 3, "region": "Lung"}, {"title": "VB1", "machine": "VB1", "start": 156, "end": 168, "patient": 3, "region": "Lung"}, {"title": "VB1", "machine": "VB1", "start": 180, "end": 192, "patient": 3, "region": "Lung"}, {"title": "VB2", "machine": "VB2", "start": 192, "end": 204, "patient": 3, "region": "Lung"}, {"title": "VB2", "machine": "VB2", "start": 204, "end": 216, "patient": 3, "region": "Lung"}, {"title": "VB2", "machine": "VB2", "start": 228, "end": 240, "patient": 3, "region": "Lung"}, {"title": "VB2", "machine": "VB2", "start": 300, "end": 312, "patient": 3, "region": "Lung"}, {"title": "VB1", "machine": "VB1", "start": 312, "end": 324, "patient": 3, "region": "Lung"}, {"title": "VB1", "machine": "VB1", "start": 336, "end": 348, "patient": 3, "region": "Lung"}, {"title": "VB2", "machine": "VB2", "start": 384, "end": 396, "patient": 3, "region": "Lung"}, {"title": "VB1", "machine": "VB1", "start": 0, "end": 12, "patient": 4, "region": "Whole_Brain"}, {"title": "VB2", "machine": "VB2", "start": 12, "end": 24, "patient": 4, "region": "Whole_Brain"}, {"title": "U", "machine": "U", "start": 24, "end": 36, "patient": 4, "region": "Whole_Brain"}, {"title": "VB2", "machine": "VB2", "start": 36, "end": 48, "patient": 4, "region": "Whole_Brain"}, {"title": "VB1", "machine": "VB1", "start": 48, "end": 60, "patient": 4, "region": "Whole_Brain"}, {"title": "VB1", "machine": "VB1", "start": 60, "end": 72, "patient": 4, "region": "Whole_Brain"}, {"title": "VB2", "machine": "VB2", "start": 72, "end": 84, "patient": 4, "region": "Whole_Brain"}, {"title": "VB2", "machine": "VB2", "start": 84, "end": 96, "patient": 4, "region": "Whole_Brain"}, {"title": "U", "machine": "U", "start": 96, "end": 108, "patient": 4, "region": "Whole_Brain"}, {"title": "VB1", "machine": "VB1", "start": 240, "end": 252, "patient": 4, "region": "Whole_Brain"}, {"title": "TB2", "machine": "TB2", "start": 0, "end": 12, "patient": 5, "region": "Craniospinal"}, {"title": "TB1", "machine": "TB1", "start": 84, "end": 96, "patient": 5, "region": "Craniospinal"}, {"title": "TB2", "machine": "TB2", "start": 132, "end": 144, "patient": 5, "region": "Craniospinal"}, {"title": "TB2", "machine": "TB2", "start": 156, "end": 168, "patient": 5, "region": "Craniospinal"}, {"title": "TB2", "machine": "TB2", "start": 168, "end": 180, "patient": 5, "region": "Craniospinal"}, {"title": "TB2", "machine": "TB2", "start": 252, "end": 264, "patient": 5, "region": "Craniospinal"}, {"title": "TB2", "machine": "TB2", "start": 264, "end": 276, "patient": 5, "region": "Craniospinal"}, {"title": "TB2", "machine": "TB2", "start": 276, "end": 288, "patient": 5, "region": "Craniospinal"}, {"title": "TB2", "machine": "TB2", "start": 300, "end": 312, "patient": 5, "region": "Craniospinal"}, {"title": "TB2", "machine": "TB2", "start": 312, "end": 324, "patient": 5, "region": "Craniospinal"}, {"title": "TB2", "machine": "TB2", "start": 324, "end": 336, "patient": 5, "region": "Craniospinal"}, {"title": "TB2", "machine": "TB2", "start": 372, "end": 384, "patient": 5, "region": "Craniospinal"}, {"title": "TB2", "machine": "TB2", "start": 396, "end": 408, "patient": 5, "region": "Craniospinal"}, {"title": "TB1", "machine": "TB1", "start": 408, "end": 420, "patient": 5, "region": "Craniospinal"}, {"title": "TB2", "machine": "TB2", "start": 432, "end": 444, "patient": 5, "region": "Craniospinal"}, {"title": "TB1", "machine": "TB1", "start": 444, "end": 456, "patient": 5, "region": "Craniospinal"}, {"title": "TB2", "machine": "TB2", "start": 456, "end": 468, "patient": 5, "region": "Craniospinal"}, {"title": "VB1", "machine": "VB1", "start": 24, "end": 36, "patient": 6, "region": "Lung"}, {"title": "VB2", "machine": "VB2", "start": 48, "end": 60, "patient": 6, "region": "Lung"}, {"title": "VB1", "machine": "VB1", "start": 72, "end": 84, "patient": 6, "region": "Lung"}, {"title": "VB1", "machine": "VB1", "start": 84, "end": 96, "patient": 6, "region": "Lung"}, {"title": "VB1", "machine": "VB1", "start": 96, "end": 108, "patient": 6, "region": "Lung"}, {"title": "VB2", "machine": "VB2", "start": 108, "end": 120, "patient": 6, "region": "Lung"}, {"title": "VB2", "machine": "VB2", "start": 120, "end": 132, "patient": 6, "region": "Lung"}, {"title": "VB1", "machine": "VB1", "start": 132, "end": 144, "patient": 6, "region": "Lung"}, {"title": "VB2", "machine": "VB2", "start": 144, "end": 156, "patient": 6, "region": "Lung"}, {"title": "VB1", "machine": "VB1", "start": 216, "end": 228, "patient": 6, "region": "Lung"}, {"title": "VB2", "machine": "VB2", "start": 264, "end": 276, "patient": 6, "region": "Lung"}, {"title": "VB2", "machine": "VB2", "start": 276, "end": 288, "patient": 6, "region": "Lung"}, {"title": "VB2", "machine": "VB2", "start": 312, "end": 324, "patient": 6, "region": "Lung"}, {"title": "VB2", "machine": "VB2", "start": 372, "end": 384, "patient": 6, "region": "Lung"}, {"title": "VB2", "machine": "VB2", "start": 420, "end": 432, "patient": 6, "region": "Lung"}, {"title": "TB1", "machine": "TB1", "start": 0, "end": 12, "patient": 7, "region": "Craniospinal"}, {"title": "TB2", "machine": "TB2", "start": 12, "end": 24, "patient": 7, "region": "Craniospinal"}, {"title": "TB2", "machine": "TB2", "start": 24, "end": 36, "patient": 7, "region": "Craniospinal"}, {"title": "TB1", "machine": "TB1", "start": 36, "end": 48, "patient": 7, "region": "Craniospinal"}, {"title": "TB2", "machine": "TB2", "start": 48, "end": 60, "patient": 7, "region": "Craniospinal"}, {"title": "TB2", "machine": "TB2", "start": 60, "end": 72, "patient": 7, "region": "Craniospinal"}, {"title": "TB2", "machine": "TB2", "start": 72, "end": 84, "patient": 7, "region": "Craniospinal"}, {"title": "TB2", "machine": "TB2", "start": 96, "end": 108, "patient": 7, "region": "Craniospinal"}, {"title": "TB2", "machine": "TB2", "start": 108, "end": 120, "patient": 7, "region": "Craniospinal"}, {"title": "TB2", "machine": "TB2", "start": 120, "end": 132, "patient": 7, "region": "Craniospinal"}, {"title": "TB1", "machine": "TB1", "start": 132, "end": 144, "patient": 7, "region": "Craniospinal"}, {"title": "TB2", "machine": "TB2", "start": 144, "end": 156, "patient": 7, "region": "Craniospinal"}, {"title": "TB1", "machine": "TB1", "start": 156, "end": 168, "patient": 7, "region": "Craniospinal"}, {"title": "TB1", "machine": "TB1", "start": 168, "end": 180, "patient": 7, "region": "Craniospinal"}, {"title": "TB2", "machine": "TB2", "start": 180, "end": 192, "patient": 7, "region": "Craniospinal"}, {"title": "TB1", "machine": "TB1", "start": 192, "end": 204, "patient": 7, "region": "Craniospinal"}, {"title": "TB2", "machine": "TB2", "start": 204, "end": 216, "patient": 7, "region": "Craniospinal"}, {"title": "TB1", "machine": "TB1", "start": 216, "end": 228, "patient": 7, "region": "Craniospinal"}, {"title": "TB1", "machine": "TB1", "start": 228, "end": 240, "patient": 7, "region": "Craniospinal"}, {"title": "TB1", "machine": "TB1", "start": 240, "end": 252, "patient": 7, "region": "Craniospinal"}, {"title": "TB1", "machine": "TB1", "start": 288, "end": 300, "patient": 7, "region": "Craniospinal"}, {"title": "TB1", "machine": "TB1", "start": 312, "end": 324, "patient": 7, "region": "Craniospinal"}, {"title": "TB1", "machine": "TB1", "start": 324, "end": 336, "patient": 7, "region": "Craniospinal"}, {"title": "TB2", "machine": "TB2", "start": 336, "end": 348, "patient": 7, "region": "Craniospinal"}, {"title": "TB2", "machine": "TB2", "start": 348, "end": 360, "patient": 7, "region": "Craniospinal"}, {"title": "TB1", "machine": "TB1", "start": 360, "end": 372, "patient": 7, "region": "Craniospinal"}, {"title": "TB1", "machine": "TB1", "start": 372, "end": 384, "patient": 7, "region": "Craniospinal"}, {"title": "TB1", "machine": "TB1", "start": 384, "end": 396, "patient": 7, "region": "Craniospinal"}, {"title": "TB2", "machine": "TB2", "start": 408, "end": 420, "patient": 7, "region": "Craniospinal"}, {"title": "TB2", "machine": "TB2", "start": 420, "end": 432, "patient": 7, "region": "Craniospinal"}, {"title": "TB1", "machine": "TB1", "start": 12, "end": 24, "patient": 8, "region": "Breast_special"}, {"title": "TB1", "machine": "TB1", "start": 24, "end": 36, "patient": 8, "region": "Breast_special"}, {"title": "TB2", "machine": "TB2", "start": 36, "end": 48, "patient": 8, "region": "Breast_special"}, {"title": "TB1", "machine": "TB1", "start": 48, "end": 60, "patient": 8, "region": "Breast_special"}, {"title": "TB1", "machine": "TB1", "start": 60, "end": 72, "patient": 8, "region": "Breast_special"}, {"title": "TB1", "machine": "TB1", "start": 72, "end": 84, "patient": 8, "region": "Breast_special"}, {"title": "TB2", "machine": "TB2", "start": 84, "end": 96, "patient": 8, "region": "Breast_special"}, {"title": "TB1", "machine": "TB1", "start": 96, "end": 108, "patient": 8, "region": "Breast_special"}, {"title": "TB1", "machine": "TB1", "start": 108, "end": 120, "patient": 8, "region": "Breast_special"}, {"title": "TB1", "machine": "TB1", "start": 120, "end": 132, "patient": 8, "region": "Breast_special"}, {"title": "TB1", "machine": "TB1", "start": 144, "end": 156, "patient": 8, "region": "Breast_special"}, {"title": "TB1", "machine": "TB1", "start": 180, "end": 192, "patient": 8, "region": "Breast_special"}, {"title": "TB2", "machine": "TB2", "start": 192, "end": 204, "patient": 8, "region": "Breast_special"}, {"title": "TB1", "machine": "TB1", "start": 204, "end": 216, "patient": 8, "region": "Breast_special"}, {"title": "TB2", "machine": "TB2", "start": 216, "end": 228, "patient": 8, "region": "Breast_special"}, {"title": "TB2", "machine": "TB2", "start": 228, "end": 240, "patient": 8, "region": "Breast_special"}, {"title": "TB2", "machine": "TB2", "start": 240, "end": 252, "patient": 8, "region": "Breast_special"}, {"title": "TB1", "machine": "TB1", "start": 252, "end": 264, "patient": 8, "region": "Breast_special"}, {"title": "TB1", "machine": "TB1", "start": 264, "end": 276, "patient": 8, "region": "Breast_special"}, {"title": "TB1", "machine": "TB1", "start": 276, "end": 288, "patient": 8, "region": "Breast_special"}, {"title": "TB2", "machine": "TB2", "start": 288, "end": 300, "patient": 8, "region": "Breast_special"}, {"title": "TB1", "machine": "TB1", "start": 300, "end": 312, "patient": 8, "region": "Breast_special"}, {"title": "TB1", "machine": "TB1", "start": 336, "end": 348, "patient": 8, "region": "Breast_special"}, {"title": "TB1", "machine": "TB1", "start": 348, "end": 360, "patient": 8, "region": "Breast_special"}, {"title": "TB2", "machine": "TB2", "start": 360, "end": 372, "patient": 8, "region": "Breast_special"}, {"title": "TB2", "machine": "TB2", "start": 384, "end": 396, "patient": 8, "region": "Breast_special"}, {"title": "TB1", "machine": "TB1", "start": 396, "end": 408, "patient": 8, "region": "Breast_special"}, {"title": "TB1", "machine": "TB1", "start": 420, "end": 432, "patient": 8, "region": "Breast_special"}, {"title": "TB1", "machine": "TB1", "start": 432, "end": 444, "patient": 8, "region": "Breast_special"}, {"title": "TB2", "machine": "TB2", "start": 444, "end": 456, "patient": 8, "region": "Breast_special"}, {"title": "VB2", "machine": "VB2", "start": 0, "end": 12, "patient": 9, "region": "Lung_special"}, {"title": "VB1", "machine": "VB1", "start": 144, "end": 156, "patient": 9, "region": "Lung_special"}, {"title": "VB1", "machine": "VB1", "start": 168, "end": 180, "patient": 9, "region": "Lung_special"}, {"title": "VB1", "machine": "VB1", "start": 228, "end": 240, "patient": 9, "region": "Lung_special"}, {"title": "VB2", "machine": "VB2", "start": 252, "end": 264, "patient": 9, "region": "Lung_special"}, {"title": "VB1", "machine": "VB1", "start": 264, "end": 276, "patient": 9, "region": "Lung_special"}, {"title": "VB1", "machine": "VB1", "start": 276, "end": 288, "patient": 9, "region": "Lung_special"}, {"title": "VB1", "machine": "VB1", "start": 300, "end": 312, "patient": 9, "region": "Lung_special"}]
    const propagateMachinesToResources = () => {
        let id = 1;
        setResources([{'id': id++, 'name': 'TB1'}, {'id': id++, 'name': 'TB2'}, {'id': id++, 'name': 'VB1'}, {'id': id++, 'name': 'VB2'}, {'id': id++, 'name': 'U'}])
    }

    const onEventResize = (data) => {
        const {start, end, event: resizedEvent} = data;

        setEvents((prevEvents) => {
            return prevEvents.map((event) => {
                if (event.id === resizedEvent.id) {
                    return {...event, start, end};
                } else {
                    return event;
                }
            });
        });
    }

    const onEventDrop = (data) => {
        const {start, end, event: droppedEvent} = data;

        setEvents((prevEvents) => {
            return prevEvents.map((event) => {
                if (event.id === droppedEvent.id) {
                    return {...event, start, end};
                } else {
                    return event;
                }
            });
        });
    }

    const mapMachineToResourceId = (machine) => {
        switch (machine) {
            case "TB1":
                return machines.TB1;
            case "TB2":
                return machines.TB2;
            case "VB1":
                return machines.VB1;
            case "VB2":
                return machines.VB2;
            case "U":
                return machines.U;
        }
    }
    const adaptEventsFromDisk = () => {
        let id = 0;
        let adaptedEvents = [];

        eventss.forEach(event => {
            console.log(events)
            let start = new Date();
            let end = new Date();
            start.setMinutes(start.getMinutes() + event.start);
            end.setMinutes(end.getMinutes() + event.end);
            adaptedEvents.push({
                id: id++,
                title: event.title + " " + event.region,
                allDay: false,
                start: start,
                end: end,
                resourceId: mapMachineToResourceId(event.machine),
                region: event.region,
                machine: event.machine,
            })
        })

        setEvents(adaptedEvents);
        console.log(adaptedEvents)
        return adaptedEvents;
    }


    const [resources, setResources] = useState([]);
    // const [events, setEvents] = useState(myEventsList);
    const [events, setEvents] = useState([]);
    const [eventsFromDisk, setEventsFromDisk] = useState([]);

    useEffect(() => {
        // setEventsFromDisk(eventsFromDisk)
        adaptEventsFromDisk();
        // fetch('/events_test.json')
        //     .then(response => response.json())
        //     .then(data => {
        //         console.log(data);
        //         setEventsFromDisk(data);
        //         adaptEventsFromDisk();
        //     })
        //     .catch(error => console.error(error));
    }, []);

    useEffect(() => {
        propagateMachinesToResources();
    }, [])

    return (
        <div className="App">
            <div>
                {/* Resizable calendar */}
                <DnDCalendar
                    localizer={localizer}
                    onEventDrop={onEventDrop}
                    step={5}
                    resources={resources}
                    resourceAccessor={'resourceId'}
                    resourceIdAccessor={'id'}
                    resourceTitleAccessor={'name'}
                    onEventResize={onEventResize}
                    defaultView="day"
                    resizable
                    style={{height: "100vh"}}
                    events={events}
                    draggableAccessor={(event) => true}
                />
            </div>
        </div>
    );
}

export default App;