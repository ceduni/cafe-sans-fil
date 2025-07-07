import { useState, useRef, useEffect } from "react";
import Container from "@/components/Layout/Container";
import { useAuth } from "@/hooks/useAuth";
import { Tab, TabList, TabPanel, TabGroup } from "@headlessui/react";
import { Fragment } from "react";
import EventBoard from "@/components/Event/EventBoard";


function Events() {
    const { user } = useAuth();
        
    const [storedEvents, setStoredEvents] = useState([]);

    function renderCreated() {
        return "created"
    }

    function renderInteracted() {
        return "interacted"
    }

    const categories = {
        "Mes évènements": renderCreated(),
        "Mes intéractions": renderInteracted()
    }

    return (
        <div className="flex">
            <Container className="ml-auto">
                    <EventBoard setStoredEvents={setStoredEvents} storedEvents={storedEvents}/>                    
            </Container>

            {/*  */}
            <div className="w-1/2 ml-auto">
                <TabGroup>
                    <TabList className="flex space-x-1 rounded-xl bg-emerald-900/20 p-1">
                        {Object.keys(categories).map((category) => (
                            <Tab as={Fragment} key={category}>
                                {({selected}) => (
                                    <button
                                    className={`w-full rounded-lg py-2.5 text-sm font-medium leading-5 
                                        ${
                                        selected
                                        ? 'bg-white shadow text-blue-700'
                                        : 'text-blue-100 hover:bg-white/[0.12] hover:text-white'
                                        }`}>
                                        {category}
                                    </button>
                                )}
                            </Tab>
                        ))}
                    </TabList>
                    {Object.values(categories).map((content, idx) => (
                        <TabPanel
                        key={idx}
                        className="rounded-xl bg-white p-4 shadow">
                        {content}
                        </TabPanel>
                    ))}
                </TabGroup>
            </div>
        </div>
    )

}



export default Events;