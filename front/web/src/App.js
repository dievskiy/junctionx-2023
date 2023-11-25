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

        eventsFromDisk.forEach(event => {
            let start = new Date();
            let end = new Date();
            start.setMinutes(start.getMinutes() + event.start);
            end.setMinutes(end.getMinutes() + event.end);
            adaptedEvents.push({
                id: id++,
                title: event.title,
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
        fetch('/events.json')
            .then(response => response.json())
            .then(data => setEventsFromDisk(data), adaptEventsFromDisk())
            .catch(error => console.error(error));
    }, [adaptEventsFromDisk]);

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
                    resources={resources}
                    resourceAccessor={'resourceId'}
                    resourceIdAccessor={'id'}
                    resourceTitleAccessor={'name'}
                    onEventResize={onEventResize}
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
