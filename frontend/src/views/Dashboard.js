import React, { Fragment, useRef, useState } from 'react';
import { Tab } from '@headlessui/react';
import UnifiedMapTab from './tabs/UnifiedMapTab';
import ThreeDMapTab from './tabs/ThreeDMapTab'; 
import TimeSeriesTab from './tabs/TimeSeriesTab';
import SeverityTab from './tabs/SeverityTab';
import PredictionTab from './tabs/PredictionTab';
import SentimentTab from './tabs/SentimentTab'; // <--- IMPORT NEW TAB
import { generatePDF } from '../utils/pdfGenerator'; 
import PublicPerception from '../components/PublicPerception';
function classNames(...classes) {
    return classes.filter(Boolean).join(' ')
}

const Dashboard = ({ activeFilters }) => {
    const dashboardRef = useRef(null);
    const [isGenerating, setIsGenerating] = useState(false);
    const totalRecords = 1000; 

    const handleExport = async () => {
        setIsGenerating(true);
        await generatePDF(activeFilters, dashboardRef, totalRecords);
        setIsGenerating(false);
    };

    const tabs = [
        "Interactive Map", 
        "3D Density", 
        "Time-Series Analysis", 
        "Severity Breakdown", 
        "Risk Prediction",
        "Public Perception" // <--- NEW TAB NAME
    ];

    return (
        <div className="w-full mt-6">
            <div className="flex justify-between items-center mb-4 px-2">
                <h2 className="text-xl font-bold text-gray-800">Dashboard View</h2>
                <button 
                    onClick={handleExport}
                    disabled={isGenerating}
                    className={`flex items-center gap-2 px-4 py-2 rounded-lg text-white font-medium transition-colors ${isGenerating ? 'bg-gray-400 cursor-not-allowed' : 'bg-red-700 hover:bg-red-800 shadow-md'}`}
                >
                    {isGenerating ? <span>⏳ Generating...</span> : <span>📄 Export Report</span>}
                </button>
            </div>

            <Tab.Group>
                <Tab.List className="flex space-x-1 rounded-xl bg-blue-900/20 p-1">
                    {tabs.map((tab) => (
                        <Tab key={tab} as={Fragment}>
                            {({ selected }) => (
                                <button
                                    className={classNames(
                                        'w-full rounded-lg py-2.5 text-sm font-medium leading-5',
                                        'ring-white/60 ring-offset-2 ring-offset-blue-400 focus:outline-none focus:ring-2',
                                        selected 
                                            ? 'bg-white text-blue-700 shadow' 
                                            : 'text-blue-100 hover:bg-white/[0.12] hover:text-white'
                                    )}
                                >
                                    {tab}
                                </button>
                            )}
                        </Tab>
                    ))}
                </Tab.List>
                
                <div ref={dashboardRef} className="mt-2 bg-white rounded-lg shadow p-6 min-h-[600px] border border-gray-200">
                    <Tab.Panels>
                        <Tab.Panel><UnifiedMapTab activeFilters={activeFilters} /></Tab.Panel>
                        <Tab.Panel><ThreeDMapTab activeFilters={activeFilters} /></Tab.Panel>
                        <Tab.Panel><TimeSeriesTab activeFilters={activeFilters} /></Tab.Panel>
                        <Tab.Panel><SeverityTab activeFilters={activeFilters} /></Tab.Panel>
                        <Tab.Panel><PredictionTab activeFilters={activeFilters} /></Tab.Panel>
                        
                        {/* NEW PANEL */}
                        <Tab.Panel><SentimentTab activeFilters={activeFilters} /></Tab.Panel>
                    </Tab.Panels>
                </div>
            </Tab.Group>
        </div>
    );
};

export default Dashboard;