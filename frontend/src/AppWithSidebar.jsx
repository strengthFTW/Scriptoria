import { useState } from 'react';
import App from './App';
import Sidebar from './components/Sidebar';
import Navbar from './components/Navbar';

function AppWithSidebar() {
    const [sidebarKey, setSidebarKey] = useState(0);
    const [selectedStory, setSelectedStory] = useState(null);

    const handleSelectStory = async (story) => {
        // Pass the story data to App component
        setSelectedStory(story);
    };

    const handleNewStory = () => {
        setSelectedStory(null);
    };

    const handleStorySaved = () => {
        setSidebarKey(prev => prev + 1);
        setSelectedStory(null);
    };

    return (
        <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh', background: '#f5f1e8' }}>
            <Navbar />
            <div style={{ display: 'flex', flex: 1 }}>
                <Sidebar
                    key={sidebarKey}
                    onSelectStory={handleSelectStory}
                    onNewStory={handleNewStory}
                />
                <div style={{ flex: 1, padding: '40px 24px' }}>
                    <App
                        initialStory={selectedStory}
                        onStorySaved={handleStorySaved}
                    />
                </div>
            </div>
        </div>
    );
}

export default AppWithSidebar;
