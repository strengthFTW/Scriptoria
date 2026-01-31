import { useState, useEffect } from 'react';
import { supabase } from '../supabaseClient';
import { useAuth } from '../context/AuthContext';
import './Sidebar.css';

function Sidebar({ onSelectStory, onNewStory }) {
    const { user } = useAuth();
    const [stories, setStories] = useState([]);
    const [loading, setLoading] = useState(true);
    const [selectedId, setSelectedId] = useState(null);

    useEffect(() => {
        if (user) {
            loadStories();
        }
    }, [user]);

    const loadStories = async () => {
        try {
            setLoading(true);
            const { data, error } = await supabase
                .from('stories')
                .select('id, title, genre, updated_at')
                .order('updated_at', { ascending: false });

            if (error) throw error;
            setStories(data || []);
        } catch (error) {
            console.error('Failed to load stories:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleSelectStory = async (storyId) => {
        try {
            setSelectedId(storyId);
            const { data, error } = await supabase
                .from('stories')
                .select('*')
                .eq('id', storyId)
                .single();

            if (error) throw error;
            onSelectStory(data);
        } catch (error) {
            console.error('Failed to load story:', error);
        }
    };

    const handleNewStory = () => {
        setSelectedId(null);
        onNewStory();
    };

    const handleDeleteStory = async (storyId, e) => {
        e.stopPropagation();
        if (!confirm('Delete this story?')) return;

        try {
            const { error } = await supabase
                .from('stories')
                .delete()
                .eq('id', storyId);

            if (error) throw error;

            setStories(prevStories => prevStories.filter(s => s.id !== storyId));
            if (selectedId === storyId) {
                handleNewStory();
            }
        } catch (error) {
            console.error('Delete failed:', error);
            alert(`Delete failed: ${error.message}`);
        }
    };

    const formatDate = (dateString) => {
        if (!dateString) return '';

        // Robust parsing for ISO strings from Supabase (handling +00:00 or missing Z)
        const date = new Date(dateString);

        // Fallback for older browsers or weird formats
        if (isNaN(date.getTime())) {
            const normalized = dateString.includes('T') ? dateString : dateString.replace(' ', 'T');
            const fixed = normalized.endsWith('Z') || normalized.includes('+') ? normalized : normalized + 'Z';
            const fallbackDate = new Date(fixed);
            if (isNaN(fallbackDate.getTime())) return 'Recently';
            return formatRelative(fallbackDate);
        }

        return formatRelative(date);
    };

    const formatRelative = (date) => {
        const now = new Date();
        const diffMs = Math.max(0, now - date);
        const diffMins = Math.floor(diffMs / 60000);
        const diffHours = Math.floor(diffMs / 3600000);
        const diffDays = Math.floor(diffMs / 86400000);

        if (diffMins < 1) return 'just now';
        if (diffMins < 60) return `${diffMins}m ago`;
        if (diffHours < 24) return `${diffHours}h ago`;
        if (diffDays < 7) return `${diffDays}d ago`;
        return date.toLocaleDateString();
    };

    return (
        <div className="sidebar">
            <div className="sidebar-header">
                <div className="sidebar-header-content">
                    <svg className="sidebar-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>
                        <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path>
                        <path d="M16 7h2"></path>
                        <path d="M16 11h2"></path>
                        <path d="M16 15h2"></path>
                        <path d="M8 7h4"></path>
                        <path d="M8 11h4"></path>
                        <path d="M8 15h4"></path>
                    </svg>
                    <div className="sidebar-title">RECENT STORIES</div>
                </div>
            </div>

            <div className="stories-list">
                {loading ? (
                    <div className="loading-state">Loading...</div>
                ) : stories.length === 0 ? (
                    <div className="empty-state">
                        <p>No stories yet.</p>
                        <p>Generate your first screenplay!</p>
                    </div>
                ) : (
                    stories.map(story => (
                        <div
                            key={story.id}
                            className={`story-card ${selectedId === story.id ? 'active' : ''}`}
                            onClick={() => handleSelectStory(story.id)}
                        >
                            {story.genre && (
                                <div className={`genre-tag genre-${story.genre.toLowerCase()}`}>
                                    {story.genre.toUpperCase()}
                                </div>
                            )}
                            <h3 className="story-title">{story.title}</h3>
                            <p className="story-date">Last edited {formatDate(story.updated_at)}</p>
                            <button
                                className="delete-btn"
                                onClick={(e) => handleDeleteStory(story.id, e)}
                                title="Delete"
                            >
                                X
                            </button>
                        </div>
                    ))
                )}
            </div>
        </div>
    );
}

export default Sidebar;
