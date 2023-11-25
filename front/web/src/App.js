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

    const [resources, setResources] = useState([]);
    const [events, setEvents] = useState(myEventsList);

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
