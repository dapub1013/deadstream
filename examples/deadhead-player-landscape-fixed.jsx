import React, { useState, useRef, useEffect } from 'react';
import { Play, Pause, SkipBack, SkipForward, Heart, Clock, Calendar, MapPin, Shuffle, Sparkles, RotateCcw, RotateCw, ChevronDown, Settings, Wifi, Volume2, Moon, Info, VolumeX } from 'lucide-react';

const DeadheadPlayerLandscape = () => {
  const [currentView, setCurrentView] = useState('player'); // 'player', 'browse', or 'settings'
  const [browseMode, setBrowseMode] = useState('top-rated');
  const [expandedState, setExpandedState] = useState(null); // Track which state is expanded
  const [expandedDecade, setExpandedDecade] = useState(null); // Track which decade is expanded
  const [isPlaying, setIsPlaying] = useState(true);
  const [currentTrack, setCurrentTrack] = useState(0);
  const [isFavorited, setIsFavorited] = useState(false);
  const [progress, setProgress] = useState(45);
  const [volume, setVolume] = useState(75); // Volume level 0-100
  const [isMuted, setIsMuted] = useState(false); // Mute state
  const [settingsSection, setSettingsSection] = useState('network'); // Which settings section is selected

  // Ref for the scrollable container
  const scrollContainerRef = useRef(null);
  const scrollPositionRef = useRef(0);

  // Save scroll position before state change
  const handleStateExpand = (stateName) => {
    if (scrollContainerRef.current) {
      scrollPositionRef.current = scrollContainerRef.current.scrollTop;
    }
    setExpandedState(expandedState === stateName ? null : stateName);
  };

  // Restore scroll position after render
  useEffect(() => {
    if (scrollContainerRef.current && scrollPositionRef.current > 0) {
      scrollContainerRef.current.scrollTop = scrollPositionRef.current;
    }
  }, [expandedState, expandedDecade]);

  // Handle decade expand/collapse
  const handleDecadeExpand = (decade) => {
    if (scrollContainerRef.current) {
      scrollPositionRef.current = scrollContainerRef.current.scrollTop;
    }
    setExpandedDecade(expandedDecade === decade ? null : decade);
  };

  // Function to skip 30 seconds backward
  const rewind30 = () => {
    // In real implementation, this would adjust the audio playback position
    setProgress(Math.max(0, progress - 10)); // Simulating with progress bar
  };

  // Function to skip 30 seconds forward
  const forward30 = () => {
    // In real implementation, this would adjust the audio playback position
    setProgress(Math.min(100, progress + 10)); // Simulating with progress bar
  };

  // Volume control functions
  const toggleMute = () => {
    setIsMuted(!isMuted);
  };

  const handleVolumeChange = (newVolume) => {
    setVolume(newVolume);
    if (newVolume > 0 && isMuted) {
      setIsMuted(false);
    }
  };

  const concert = {
    date: '1977/05/08',
    venue: 'Barton Hall, Cornell University',
    city: 'Ithaca',
    state: 'NY',
    source: 'Soundboard',
    rating: 4.8
  };

  const setlist = [
    { id: 1, name: "New Minglewood Blues", duration: "5:42", set: "Set I" },
    { id: 2, name: "Loser", duration: "7:08", set: "Set I" },
    { id: 3, name: "El Paso", duration: "4:38", set: "Set I" },
    { id: 4, name: "They Love Each Other", duration: "7:26", set: "Set I" },
    { id: 5, name: "Jack Straw", duration: "5:15", set: "Set I" },
    { id: 6, name: "Deal", duration: "5:26", set: "Set I" },
    { id: 7, name: "Lazy Lightning", duration: "3:17", set: "Set I" },
    { id: 8, name: "Supplication", duration: "4:52", set: "Set I" },
    { id: 9, name: "Brown-Eyed Women", duration: "5:25", set: "Set I" },
    { id: 10, name: "Mama Tried", duration: "2:40", set: "Set I" },
    { id: 11, name: "Row Jimmy", duration: "9:50", set: "Set I" },
    { id: 12, name: "Dancing in the Streets", duration: "14:26", set: "Set I" },
    { id: 13, name: "Scarlet Begonias", duration: "10:22", set: "Set II" },
    { id: 14, name: "Fire on the Mountain", duration: "14:51", set: "Set II" },
    { id: 15, name: "Estimated Prophet", duration: "11:45", set: "Set II" },
    { id: 16, name: "St. Stephen", duration: "6:42", set: "Set II" },
    { id: 17, name: "Not Fade Away", duration: "8:15", set: "Set II" },
    { id: 18, name: "St. Stephen", duration: "1:28", set: "Set II" },
    { id: 19, name: "Morning Dew", duration: "11:51", set: "Set II" },
    { id: 20, name: "One More Saturday Night", duration: "4:58", set: "Encore" }
  ];

  const browseShows = [
    { date: '1977/05/08', venue: 'Barton Hall, Cornell', location: 'Ithaca, NY', rating: 4.8 },
    { date: '1972/05/26', venue: 'The Strand Lyceum', location: 'London, UK', rating: 4.7 },
    { date: '1989/07/07', venue: 'JFK Stadium', location: 'Philadelphia, PA', rating: 4.6 },
    { date: '1970/02/13', venue: 'Fillmore East', location: 'New York, NY', rating: 4.5 },
    { date: '1974/06/18', venue: 'Freedom Hall', location: 'Louisville, KY', rating: 4.7 },
    { date: '1977/05/09', venue: 'Buffalo Memorial Auditorium', location: 'Buffalo, NY', rating: 4.6 },
    { date: '1973/11/10', venue: 'Winterland Arena', location: 'San Francisco, CA', rating: 4.5 },
  ];

  const onThisDayShows = [
    { date: '1986/12/15', venue: 'Oakland Coliseum Arena', location: 'Oakland, CA', rating: 4.3, yearsAgo: 39 },
    { date: '1978/12/15', venue: 'Veterans Memorial Coliseum', location: 'New Haven, CT', rating: 4.2, yearsAgo: 47 },
    { date: '1971/12/15', venue: 'Hill Auditorium', location: 'Ann Arbor, MI', rating: 4.4, yearsAgo: 54 },
    { date: '1969/12/15', venue: 'Fillmore Auditorium', location: 'San Francisco, CA', rating: 4.1, yearsAgo: 56 },
  ];

  // Check if there are shows for today
  const hasShowsToday = onThisDayShows.length > 0;

  // Venue data - organized by importance and location
  const famousVenues = [
    { name: 'Fillmore West', location: 'San Francisco, CA', shows: 47, rating: 4.6 },
    { name: 'Winterland Arena', location: 'San Francisco, CA', shows: 53, rating: 4.5 },
    { name: 'Red Rocks Amphitheatre', location: 'Morrison, CO', shows: 23, rating: 4.7 },
    { name: 'Barton Hall, Cornell University', location: 'Ithaca, NY', shows: 1, rating: 4.9 },
    { name: 'Madison Square Garden', location: 'New York, NY', shows: 52, rating: 4.4 },
    { name: 'Capitol Theatre', location: 'Port Chester, NY', shows: 43, rating: 4.6 },
    { name: 'The Spectrum', location: 'Philadelphia, PA', shows: 53, rating: 4.5 },
    { name: 'Greek Theatre', location: 'Berkeley, CA', shows: 65, rating: 4.5 },
    { name: 'Fillmore East', location: 'New York, NY', shows: 43, rating: 4.7 },
    { name: 'Oakland Coliseum Arena', location: 'Oakland, CA', shows: 67, rating: 4.3 },
  ];

  const venuesByState = [
    { 
      state: 'California', 
      count: 342,
      venues: [
        { name: 'Fillmore West', location: 'San Francisco', shows: 47 },
        { name: 'Winterland Arena', location: 'San Francisco', shows: 53 },
        { name: 'Greek Theatre', location: 'Berkeley', shows: 65 },
        { name: 'Oakland Coliseum Arena', location: 'Oakland', shows: 67 },
        { name: 'Frost Amphitheatre', location: 'Stanford', shows: 12 },
        { name: 'Ventura County Fairgrounds', location: 'Ventura', shows: 8 },
      ]
    },
    { 
      state: 'New York', 
      count: 187,
      venues: [
        { name: 'Madison Square Garden', location: 'New York', shows: 52 },
        { name: 'Capitol Theatre', location: 'Port Chester', shows: 43 },
        { name: 'Fillmore East', location: 'New York', shows: 43 },
        { name: 'Nassau Coliseum', location: 'Uniondale', shows: 35 },
      ]
    },
    { 
      state: 'Colorado', 
      count: 89,
      venues: [
        { name: 'Red Rocks Amphitheatre', location: 'Morrison', shows: 23 },
        { name: 'McNichols Sports Arena', location: 'Denver', shows: 18 },
        { name: 'Folsom Field', location: 'Boulder', shows: 8 },
      ]
    },
    { 
      state: 'Pennsylvania', 
      count: 76,
      venues: [
        { name: 'The Spectrum', location: 'Philadelphia', shows: 53 },
        { name: 'Civic Arena', location: 'Pittsburgh', shows: 12 },
      ]
    },
    { 
      state: 'Illinois', 
      count: 64,
      venues: [
        { name: 'Chicago Stadium', location: 'Chicago', shows: 23 },
        { name: 'Rosemont Horizon', location: 'Rosemont', shows: 15 },
      ]
    },
  ];

  // Year browse data - legendary years and decades
  const legendaryYears = [
    { year: '1977', shows: 97, rating: 4.7, note: 'The peak! ⚡' },
    { year: '1972', shows: 156, rating: 4.6, note: "Europe '72" },
    { year: '1973', shows: 71, rating: 4.5, note: 'Wake of the Flood' },
    { year: '1989', shows: 73, rating: 4.4, note: 'Return to form' },
    { year: '1969', shows: 141, rating: 4.5, note: 'Live/Dead era' },
  ];

  const showsByDecade = [
    {
      decade: '1960s',
      count: 348,
      years: [
        { year: '1965', shows: 6 },
        { year: '1966', shows: 74 },
        { year: '1967', shows: 67 },
        { year: '1968', shows: 60 },
        { year: '1969', shows: 141 },
      ]
    },
    {
      decade: '1970s',
      count: 892,
      years: [
        { year: '1970', shows: 143 },
        { year: '1971', shows: 122 },
        { year: '1972', shows: 156 },
        { year: '1973', shows: 71 },
        { year: '1974', shows: 40 },
        { year: '1975', shows: 4 },
        { year: '1976', shows: 41 },
        { year: '1977', shows: 97 },
        { year: '1978', shows: 114 },
        { year: '1979', shows: 104 },
      ]
    },
    {
      decade: '1980s',
      count: 634,
      years: [
        { year: '1980', shows: 86 },
        { year: '1981', shows: 78 },
        { year: '1982', shows: 60 },
        { year: '1983', shows: 69 },
        { year: '1984', shows: 62 },
        { year: '1985', shows: 75 },
        { year: '1987', shows: 78 },
        { year: '1988', shows: 77 },
        { year: '1989', shows: 73 },
      ]
    },
    {
      decade: '1990s',
      count: 412,
      years: [
        { year: '1990', shows: 80 },
        { year: '1991', shows: 75 },
        { year: '1992', shows: 64 },
        { year: '1993', shows: 78 },
        { year: '1994', shows: 84 },
        { year: '1995', shows: 31 },
      ]
    },
  ];

  const PlayerScreen = () => (
    <div className="flex h-full bg-black text-white">
      {/* Left Side - Setlist */}
      <div className="w-1/2 border-r border-gray-800 flex flex-col">
        <div className="px-6 py-5 border-b border-gray-800">
          <div className="flex items-start justify-between mb-3">
            <div className="flex-1 min-w-0">
              <h1 className="text-2xl font-semibold mb-1">
                {concert.date} {concert.venue}
              </h1>
              <p className="text-gray-400 text-lg">
                {concert.city}, {concert.state}
              </p>
            </div>
            <button 
              onClick={() => setIsFavorited(!isFavorited)}
              className="ml-4 p-2 rounded-full hover:bg-gray-800 transition-colors"
            >
              <Heart 
                className={`w-7 h-7 ${isFavorited ? 'fill-red-500 text-red-500' : 'text-gray-400'}`}
              />
            </button>
          </div>
          <div className="flex items-center gap-4 text-sm text-gray-400">
            <span className="bg-gray-800 px-3 py-1 rounded-full">{concert.source}</span>
            <span>★ {concert.rating}/5.0</span>
            <span className="text-gray-600">•</span>
            <span>{setlist.length} tracks</span>
          </div>
        </div>

        <div className="flex-1 overflow-y-auto px-6 py-4">
          {setlist.map((track, index) => {
            const isCurrentTrack = index === currentTrack;
            const lastSet = index === 0 ? null : setlist[index - 1].set;
            const showSetHeader = track.set !== lastSet;

            return (
              <div key={track.id}>
                {showSetHeader && (
                  <div className="text-gray-500 text-sm font-semibold mt-4 mb-2 uppercase tracking-wider">
                    {track.set}
                  </div>
                )}
                <div
                  onClick={() => setCurrentTrack(index)}
                  className={`flex items-center justify-between py-3 px-3 rounded-lg cursor-pointer transition-colors ${
                    isCurrentTrack 
                      ? 'bg-gray-800 text-white' 
                      : 'hover:bg-gray-900 text-gray-300'
                  }`}
                >
                  <div className="flex items-center gap-4 flex-1 min-w-0">
                    <span className="text-gray-500 text-sm w-6">{track.id}</span>
                    <span className={`truncate ${isCurrentTrack ? 'font-semibold' : ''}`}>
                      {track.name}
                    </span>
                  </div>
                  <span className="text-gray-500 text-sm ml-4">{track.duration}</span>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Right Side - Player Controls */}
      <div className="w-1/2 flex flex-col">
        <div className="flex-1 flex flex-col justify-center px-8 py-6">
          <div className="mb-8">
            <div className="text-sm text-gray-500 mb-2 uppercase tracking-wider">Now Playing</div>
            <div className="text-3xl font-bold mb-2">{setlist[currentTrack].name}</div>
            <div className="text-xl text-gray-400">{setlist[currentTrack].set}</div>
          </div>

          <div className="mb-8">
            <input
              type="range"
              min="0"
              max="100"
              value={progress}
              onChange={(e) => setProgress(parseInt(e.target.value))}
              className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer"
              style={{
                background: `linear-gradient(to right, #3b82f6 0%, #3b82f6 ${progress}%, #374151 ${progress}%, #374151 100%)`
              }}
            />
            <div className="flex justify-between text-sm text-gray-500 mt-2">
              <span>3:42</span>
              <span>{setlist[currentTrack].duration}</span>
            </div>
          </div>

          <div className="flex flex-col items-center gap-4 mb-8">
            {/* Main playback controls */}
            <div className="flex items-center justify-center gap-6">
              <button 
                onClick={() => setCurrentTrack(Math.max(0, currentTrack - 1))}
                className="p-4 hover:bg-gray-800 rounded-full transition-colors"
                disabled={currentTrack === 0}
                title="Previous track"
              >
                <SkipBack className={`w-9 h-9 ${currentTrack === 0 ? 'text-gray-700' : ''}`} />
              </button>
              
              <button 
                onClick={() => setIsPlaying(!isPlaying)}
                className="p-6 bg-white text-black rounded-full hover:bg-gray-200 transition-colors"
                title={isPlaying ? "Pause" : "Play"}
              >
                {isPlaying ? <Pause className="w-12 h-12" /> : <Play className="w-12 h-12 ml-1" />}
              </button>
              
              <button 
                onClick={() => setCurrentTrack(Math.min(setlist.length - 1, currentTrack + 1))}
                className="p-4 hover:bg-gray-800 rounded-full transition-colors"
                disabled={currentTrack === setlist.length - 1}
                title="Next track"
              >
                <SkipForward className={`w-9 h-9 ${currentTrack === setlist.length - 1 ? 'text-gray-700' : ''}`} />
              </button>
            </div>

            {/* 30-second skip controls */}
            <div className="flex items-center gap-4">
              <button 
                onClick={rewind30}
                className="flex items-center gap-2 px-4 py-2 bg-gray-800 hover:bg-gray-700 rounded-lg transition-colors"
                title="Rewind 30 seconds"
              >
                <RotateCcw className="w-5 h-5" />
                <span className="text-sm font-semibold">30s</span>
              </button>
              
              <button 
                onClick={forward30}
                className="flex items-center gap-2 px-4 py-2 bg-gray-800 hover:bg-gray-700 rounded-lg transition-colors"
                title="Skip forward 30 seconds"
              >
                <span className="text-sm font-semibold">30s</span>
                <RotateCw className="w-5 h-5" />
              </button>
            </div>
          </div>

          <div className="text-center text-sm text-gray-500 mb-6">
            Track {currentTrack + 1} of {setlist.length}
          </div>

          {/* Volume Control */}
          <div className="px-4">
            <div className="flex items-center gap-4 mb-2">
              <button 
                onClick={toggleMute}
                className="p-2 hover:bg-gray-800 rounded-full transition-colors"
                title={isMuted ? "Unmute" : "Mute"}
              >
                {isMuted ? (
                  <VolumeX className="w-6 h-6 text-gray-400" />
                ) : (
                  <Volume2 className="w-6 h-6 text-gray-400" />
                )}
              </button>
              
              <input
                type="range"
                min="0"
                max="100"
                value={isMuted ? 0 : volume}
                onChange={(e) => handleVolumeChange(parseInt(e.target.value))}
                className="flex-1 h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer"
                style={{
                  background: `linear-gradient(to right, #3b82f6 0%, #3b82f6 ${isMuted ? 0 : volume}%, #374151 ${isMuted ? 0 : volume}%, #374151 100%)`
                }}
              />
              
              <span className="text-sm text-gray-400 w-12 text-right">
                {isMuted ? 0 : volume}%
              </span>
            </div>
          </div>
        </div>

        <div className="border-t border-gray-800 p-6">
          <button 
            onClick={() => setCurrentView('browse')}
            className="w-full py-4 bg-gray-800 hover:bg-gray-700 rounded-lg font-semibold text-lg transition-colors"
          >
            Browse Shows
          </button>
        </div>
      </div>
    </div>
  );

  const BrowseScreen = () => (
    <div className="flex h-full bg-black text-white">
      {/* Left Side - Browse Options */}
      <div className="w-2/5 border-r border-gray-800 flex flex-col">
        <div className="px-6 py-5 border-b border-gray-800">
          <h1 className="text-3xl font-bold mb-4">Browse Shows</h1>
          
          <div className="flex flex-col gap-2">
            <button className="px-4 py-3 bg-blue-600 rounded-lg font-semibold text-left">All Shows</button>
            <button className="px-4 py-3 bg-gray-800 hover:bg-gray-700 rounded-lg transition-colors text-left">
              <Heart className="w-5 h-5 inline mr-2" />
              Favorites
            </button>
            <button className="px-4 py-3 bg-gray-800 hover:bg-gray-700 rounded-lg transition-colors text-left">
              <Shuffle className="w-5 h-5 inline mr-2" />
              Random Show
            </button>
            <button 
              onClick={() => setCurrentView('settings')}
              className="px-4 py-3 bg-gray-800 hover:bg-gray-700 rounded-lg transition-colors text-left"
            >
              <Settings className="w-5 h-5 inline mr-2" />
              Settings
            </button>
          </div>
        </div>

        <div className="px-6 py-6 border-b border-gray-800">
          <h2 className="text-sm font-semibold text-gray-400 mb-3 uppercase tracking-wider">Browse By</h2>
          <div className="flex flex-col gap-2">
            <button 
              onClick={() => hasShowsToday && setBrowseMode('on-this-day')}
              disabled={!hasShowsToday}
              className={`flex items-center gap-3 p-4 rounded-lg transition-colors ${
                !hasShowsToday
                  ? 'bg-gray-900 opacity-50 cursor-not-allowed'
                  : browseMode === 'on-this-day' 
                    ? 'bg-orange-600 hover:bg-orange-700' 
                    : 'bg-gray-900 hover:bg-gray-800'
              }`}
              title={!hasShowsToday ? 'No shows on this date' : ''}
            >
              <Sparkles className={`w-6 h-6 ${hasShowsToday ? 'text-orange-300' : 'text-gray-600'}`} />
              <div className="text-left">
                <div className="font-semibold">On This Day</div>
                <div className={`text-xs ${hasShowsToday ? 'text-gray-300' : 'text-gray-600'}`}>
                  December 15th {!hasShowsToday && '(No shows)'}
                </div>
              </div>
            </button>
            <button 
              onClick={() => setBrowseMode('top-rated')}
              className={`flex items-center gap-3 p-4 rounded-lg transition-colors ${
                browseMode === 'top-rated' 
                  ? 'bg-gray-700' 
                  : 'bg-gray-900 hover:bg-gray-800'
              }`}
            >
              <Calendar className="w-6 h-6 text-blue-500" />
              <span className="font-semibold">Date</span>
            </button>
            <button 
              onClick={() => setBrowseMode('venue')}
              className={`flex items-center gap-3 p-4 rounded-lg transition-colors ${
                browseMode === 'venue' 
                  ? 'bg-gray-700' 
                  : 'bg-gray-900 hover:bg-gray-800'
              }`}
            >
              <MapPin className="w-6 h-6 text-green-500" />
              <span className="font-semibold">Venue</span>
            </button>
            <button 
              onClick={() => setBrowseMode('year')}
              className={`flex items-center gap-3 p-4 rounded-lg transition-colors ${
                browseMode === 'year' 
                  ? 'bg-gray-700' 
                  : 'bg-gray-900 hover:bg-gray-800'
              }`}
            >
              <Clock className="w-6 h-6 text-purple-500" />
              <span className="font-semibold">Year</span>
            </button>
          </div>
        </div>

        <div className="flex-1 px-6 py-6">
          <div className="text-sm text-gray-500">
            <div className="mb-3">
              <span className="text-2xl font-bold text-white">2,318</span>
              <span className="ml-2">shows available</span>
            </div>
            <div className="mb-3">
              <span className="text-2xl font-bold text-white">12</span>
              <span className="ml-2">favorites</span>
            </div>
            <div>
              <span className="text-gray-400">Last played:</span>
              <div className="text-white mt-1">1977/05/08 Cornell</div>
            </div>
          </div>
        </div>
      </div>

      {/* Right Side - Show List */}
      <div className="w-3/5 flex flex-col">
        <div className="px-6 py-5 border-b border-gray-800">
          {browseMode === 'on-this-day' ? (
            <>
              <h2 className="text-2xl font-bold mb-3 flex items-center gap-3">
                <Sparkles className="w-7 h-7 text-orange-400" />
                On This Day in Grateful Dead History
              </h2>
              <div className="text-sm text-gray-400">
                December 15th • Shows throughout the years on this date
              </div>
            </>
          ) : browseMode === 'venue' ? (
            <>
              <h2 className="text-2xl font-bold mb-3 flex items-center gap-3">
                <MapPin className="w-7 h-7 text-green-500" />
                Browse by Venue
              </h2>
              <div className="text-sm text-gray-400">
                Legendary venues and shows organized by location
              </div>
            </>
          ) : browseMode === 'year' ? (
            <>
              <h2 className="text-2xl font-bold mb-3 flex items-center gap-3">
                <Clock className="w-7 h-7 text-purple-500" />
                Browse by Year
              </h2>
              <div className="text-sm text-gray-400">
                Legendary years and shows organized by decade
              </div>
            </>
          ) : (
            <>
              <h2 className="text-2xl font-bold mb-3">Top Rated Shows</h2>
              <div className="text-sm text-gray-400">
                Showing the highest-rated performances from the collection
              </div>
            </>
          )}
        </div>

        <div ref={scrollContainerRef} className="flex-1 overflow-y-auto px-6 py-4">
          {browseMode === 'on-this-day' ? (
            onThisDayShows.length > 0 ? (
              onThisDayShows.map((show, index) => (
                <div
                  key={index}
                  onClick={() => setCurrentView('player')}
                  className="flex items-center justify-between p-5 mb-3 bg-gradient-to-r from-gray-900 to-gray-800 hover:from-gray-800 hover:to-gray-700 rounded-lg cursor-pointer transition-colors border border-orange-900/30"
                >
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-3 mb-1">
                      <div className="text-xl font-semibold">{show.date}</div>
                      <span className="text-sm text-orange-400 bg-orange-950/50 px-2 py-1 rounded">
                        {show.yearsAgo} years ago
                      </span>
                    </div>
                    <div className="text-gray-400 text-lg mb-1">{show.venue}</div>
                    <div className="text-sm text-gray-500">{show.location}</div>
                  </div>
                  <div className="ml-6 flex flex-col items-end gap-1">
                    <div className="flex items-center gap-2">
                      <span className="text-yellow-500 text-xl">★</span>
                      <span className="font-bold text-xl">{show.rating}</span>
                    </div>
                    <button className="text-sm text-orange-400 hover:text-orange-300">
                      Play →
                    </button>
                  </div>
                </div>
              ))
            ) : (
              <div className="text-center py-12 text-gray-500">
                <Sparkles className="w-12 h-12 mx-auto mb-4 text-gray-700" />
                <p>No shows on this date in Dead history</p>
              </div>
            )
          ) : browseMode === 'venue' ? (
            // Venue Browse View
            <>
              {/* Famous Venues Section */}
              <div className="mb-6">
                <h3 className="text-lg font-bold text-gray-400 mb-3 uppercase tracking-wider flex items-center gap-2">
                  <span className="text-yellow-500">⭐</span>
                  Legendary Venues
                </h3>
                {famousVenues.map((venue, index) => (
                  <div
                    key={index}
                    onClick={() => setCurrentView('player')}
                    className="flex items-center justify-between p-4 mb-2 bg-gray-900 hover:bg-gray-800 rounded-lg cursor-pointer transition-colors"
                  >
                    <div className="flex-1 min-w-0">
                      <div className="text-lg font-semibold mb-1">{venue.name}</div>
                      <div className="text-sm text-gray-500">{venue.location}</div>
                    </div>
                    <div className="ml-4 flex items-center gap-4">
                      <div className="text-right">
                        <div className="text-sm text-gray-400">{venue.shows} shows</div>
                        <div className="flex items-center gap-1 text-sm">
                          <span className="text-yellow-500">★</span>
                          <span className="text-white">{venue.rating}</span>
                        </div>
                      </div>
                      <button className="text-sm text-green-500 hover:text-green-400">
                        →
                      </button>
                    </div>
                  </div>
                ))}
              </div>

              {/* Venues by State Section */}
              <div>
                <h3 className="text-lg font-bold text-gray-400 mb-3 uppercase tracking-wider flex items-center gap-2">
                  <MapPin className="w-5 h-5" />
                  By State
                </h3>
                {venuesByState.map((stateData, index) => (
                  <div key={index} className="mb-2">
                    <button
                      onClick={() => handleStateExpand(stateData.state)}
                      className="w-full flex items-center justify-between p-4 bg-gray-900 hover:bg-gray-800 rounded-lg transition-colors"
                      type="button"
                    >
                      <div className="flex items-center gap-3">
                        <ChevronDown 
                          className={`w-5 h-5 text-gray-500 transition-transform ${
                            expandedState === stateData.state ? 'rotate-180' : ''
                          }`}
                        />
                        <span className="font-semibold text-lg">{stateData.state}</span>
                      </div>
                      <div className="text-sm text-gray-400">
                        {stateData.count} shows
                      </div>
                    </button>
                    
                    {/* Expanded venue list for this state */}
                    {expandedState === stateData.state && (
                      <div className="mt-2 ml-4 space-y-1">
                        {stateData.venues.map((venue, vIndex) => (
                          <div
                            key={vIndex}
                            onClick={() => setCurrentView('player')}
                            className="flex items-center justify-between p-3 bg-gray-800 hover:bg-gray-700 rounded-lg cursor-pointer transition-colors"
                          >
                            <div className="flex-1 min-w-0">
                              <div className="font-semibold">{venue.name}</div>
                              <div className="text-sm text-gray-500">{venue.location}</div>
                            </div>
                            <div className="ml-4 flex items-center gap-2">
                              <span className="text-sm text-gray-400">{venue.shows} shows</span>
                              <button className="text-sm text-green-500">→</button>
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </>
          ) : browseMode === 'year' ? (
            // Year Browse View
            <>
              {/* Legendary Years Section */}
              <div className="mb-6">
                <h3 className="text-lg font-bold text-gray-400 mb-3 uppercase tracking-wider flex items-center gap-2">
                  <span className="text-yellow-500">⭐</span>
                  Legendary Years
                </h3>
                {legendaryYears.map((yearData, index) => (
                  <div
                    key={index}
                    onClick={() => setCurrentView('player')}
                    className="flex items-center justify-between p-4 mb-2 bg-gray-900 hover:bg-gray-800 rounded-lg cursor-pointer transition-colors"
                  >
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-3 mb-1">
                        <span className="text-xl font-semibold">{yearData.year}</span>
                        <span className="text-sm text-purple-400">{yearData.note}</span>
                      </div>
                      <div className="text-sm text-gray-500">{yearData.shows} shows</div>
                    </div>
                    <div className="ml-4 flex items-center gap-4">
                      <div className="text-right">
                        <div className="flex items-center gap-1 text-sm">
                          <span className="text-yellow-500">★</span>
                          <span className="text-white">{yearData.rating}</span>
                        </div>
                      </div>
                      <button className="text-sm text-purple-500 hover:text-purple-400">
                        →
                      </button>
                    </div>
                  </div>
                ))}
              </div>

              {/* Years by Decade Section */}
              <div>
                <h3 className="text-lg font-bold text-gray-400 mb-3 uppercase tracking-wider flex items-center gap-2">
                  <Clock className="w-5 h-5" />
                  By Decade
                </h3>
                {showsByDecade.map((decadeData, index) => (
                  <div key={index} className="mb-2">
                    <button
                      onClick={() => handleDecadeExpand(decadeData.decade)}
                      className="w-full flex items-center justify-between p-4 bg-gray-900 hover:bg-gray-800 rounded-lg transition-colors"
                      type="button"
                    >
                      <div className="flex items-center gap-3">
                        <ChevronDown 
                          className={`w-5 h-5 text-gray-500 transition-transform ${
                            expandedDecade === decadeData.decade ? 'rotate-180' : ''
                          }`}
                        />
                        <span className="font-semibold text-lg">{decadeData.decade}</span>
                      </div>
                      <div className="text-sm text-gray-400">
                        {decadeData.count} shows
                      </div>
                    </button>
                    
                    {/* Expanded year list for this decade */}
                    {expandedDecade === decadeData.decade && (
                      <div className="mt-2 ml-4 space-y-1">
                        {decadeData.years.map((year, yIndex) => (
                          <div
                            key={yIndex}
                            onClick={() => setCurrentView('player')}
                            className="flex items-center justify-between p-3 bg-gray-800 hover:bg-gray-700 rounded-lg cursor-pointer transition-colors"
                          >
                            <div className="flex-1 min-w-0">
                              <div className="font-semibold text-lg">{year.year}</div>
                            </div>
                            <div className="ml-4 flex items-center gap-2">
                              <span className="text-sm text-gray-400">{year.shows} shows</span>
                              <button className="text-sm text-purple-500">→</button>
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </>
          ) : (
            // Top Rated Shows (default view)
            browseShows.map((show, index) => (
              <div
                key={index}
                onClick={() => setCurrentView('player')}
                className="flex items-center justify-between p-5 mb-3 bg-gray-900 hover:bg-gray-800 rounded-lg cursor-pointer transition-colors"
              >
                <div className="flex-1 min-w-0">
                  <div className="text-xl font-semibold mb-1">{show.date}</div>
                  <div className="text-gray-400 text-lg mb-1">{show.venue}</div>
                  <div className="text-sm text-gray-500">{show.location}</div>
                </div>
                <div className="ml-6 flex flex-col items-end gap-1">
                  <div className="flex items-center gap-2">
                    <span className="text-yellow-500 text-xl">★</span>
                    <span className="font-bold text-xl">{show.rating}</span>
                  </div>
                  <button className="text-sm text-blue-500 hover:text-blue-400">
                    Play →
                  </button>
                </div>
              </div>
            ))
          )}
        </div>

        <div className="border-t border-gray-800 p-6">
          <button 
            onClick={() => setCurrentView('player')}
            className="w-full py-4 bg-blue-600 hover:bg-blue-700 rounded-lg font-semibold text-lg transition-colors"
          >
            ← Back to Now Playing
          </button>
        </div>
      </div>
    </div>
  );

  const SettingsScreen = () => (
    <div className="flex h-full bg-black text-white">
      {/* Left Side - Settings Categories */}
      <div className="w-2/5 border-r border-gray-800 flex flex-col">
        <div className="px-6 py-5 border-b border-gray-800">
          <h1 className="text-3xl font-bold mb-2">Settings</h1>
          <p className="text-gray-400 text-sm">Device configuration and preferences</p>
        </div>

        <div className="flex-1 overflow-y-auto px-6 py-6">
          <div className="space-y-2">
            <div 
              onClick={() => setSettingsSection('network')}
              className={`p-4 rounded-lg cursor-pointer transition-colors ${
                settingsSection === 'network' ? 'bg-blue-600' : 'bg-gray-900 hover:bg-gray-800'
              }`}
            >
              <div className="flex items-center gap-3">
                <Wifi className={`w-6 h-6 ${settingsSection === 'network' ? '' : 'text-gray-400'}`} />
                <span className="font-semibold text-lg">Network</span>
              </div>
            </div>
            
            <div className="p-4 bg-gray-900 hover:bg-gray-800 rounded-lg cursor-pointer transition-colors">
              <div className="flex items-center gap-3">
                <Volume2 className="w-6 h-6 text-gray-400" />
                <span className="font-semibold text-lg">Audio</span>
              </div>
            </div>
            
            <div className="p-4 bg-gray-900 hover:bg-gray-800 rounded-lg cursor-pointer transition-colors">
              <div className="flex items-center gap-3">
                <Moon className="w-6 h-6 text-gray-400" />
                <span className="font-semibold text-lg">Display</span>
              </div>
            </div>
            
            <div className="p-4 bg-gray-900 hover:bg-gray-800 rounded-lg cursor-pointer transition-colors">
              <div className="flex items-center gap-3">
                <Clock className="w-6 h-6 text-gray-400" />
                <span className="font-semibold text-lg">Date & Time</span>
              </div>
            </div>
            
            <div 
              onClick={() => setSettingsSection('about')}
              className={`p-4 rounded-lg cursor-pointer transition-colors ${
                settingsSection === 'about' ? 'bg-blue-600' : 'bg-gray-900 hover:bg-gray-800'
              }`}
            >
              <div className="flex items-center gap-3">
                <Info className={`w-6 h-6 ${settingsSection === 'about' ? '' : 'text-gray-400'}`} />
                <span className="font-semibold text-lg">About</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Right Side - Settings Details */}
      <div className="w-3/5 flex flex-col">
        {settingsSection === 'network' ? (
          <>
            <div className="px-6 py-5 border-b border-gray-800">
              <h2 className="text-2xl font-bold mb-2 flex items-center gap-3">
                <Wifi className="w-7 h-7 text-blue-500" />
                Network Settings
              </h2>
              <p className="text-sm text-gray-400">Manage WiFi and network connections</p>
            </div>

            <div className="flex-1 overflow-y-auto px-6 py-6">
          {/* WiFi Status */}
          <div className="mb-6 p-5 bg-gray-900 rounded-lg">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-3">
                <Wifi className="w-6 h-6 text-blue-500" />
                <span className="font-semibold text-lg">WiFi</span>
              </div>
              <div className="flex items-center gap-3">
                <span className="text-sm text-green-400">Connected</span>
                <div className="w-12 h-6 bg-blue-600 rounded-full relative cursor-pointer">
                  <div className="absolute right-1 top-1 w-4 h-4 bg-white rounded-full"></div>
                </div>
              </div>
            </div>
            <div className="text-sm text-gray-400">
              <div className="mb-2">Network: <span className="text-white">DeadheadHome_5G</span></div>
              <div className="mb-2">Signal: <span className="text-white">Excellent (4 bars)</span></div>
              <div>IP Address: <span className="text-white">192.168.1.142</span></div>
            </div>
          </div>

          {/* Available Networks */}
          <div className="mb-4">
            <h3 className="text-lg font-semibold mb-3 text-gray-400">Available Networks</h3>
            <div className="space-y-2">
              <div className="p-4 bg-blue-900/30 border border-blue-700 rounded-lg">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <Wifi className="w-5 h-5 text-blue-500" />
                    <div>
                      <div className="font-semibold">DeadheadHome_5G</div>
                      <div className="text-sm text-gray-400">Connected</div>
                    </div>
                  </div>
                  <div className="text-sm text-blue-500">✓</div>
                </div>
              </div>

              <div className="p-4 bg-gray-900 hover:bg-gray-800 rounded-lg cursor-pointer transition-colors">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <Wifi className="w-5 h-5 text-gray-400" />
                    <div>
                      <div className="font-semibold">DeadheadHome_2.4G</div>
                      <div className="text-sm text-gray-400">Saved</div>
                    </div>
                  </div>
                  <div className="text-sm text-gray-500">●●●○</div>
                </div>
              </div>

              <div className="p-4 bg-gray-900 hover:bg-gray-800 rounded-lg cursor-pointer transition-colors">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <Wifi className="w-5 h-5 text-gray-400" />
                    <div>
                      <div className="font-semibold">Neighbor_WiFi</div>
                      <div className="text-sm text-gray-400">🔒 Secured</div>
                    </div>
                  </div>
                  <div className="text-sm text-gray-500">●●○○</div>
                </div>
              </div>

              <div className="p-4 bg-gray-900 hover:bg-gray-800 rounded-lg cursor-pointer transition-colors">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <Wifi className="w-5 h-5 text-gray-400" />
                    <div>
                      <div className="font-semibold">xfinitywifi</div>
                      <div className="text-sm text-gray-400">Public</div>
                    </div>
                  </div>
                  <div className="text-sm text-gray-500">●○○○</div>
                </div>
              </div>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex gap-3">
            <button className="flex-1 py-3 bg-blue-600 hover:bg-blue-700 rounded-lg font-semibold transition-colors">
              Refresh Networks
            </button>
            <button className="flex-1 py-3 bg-gray-800 hover:bg-gray-700 rounded-lg font-semibold transition-colors">
              Advanced Settings
            </button>
          </div>
        </div>
        </>
        ) : settingsSection === 'about' ? (
          <>
            <div className="px-6 py-5 border-b border-gray-800">
              <h2 className="text-2xl font-bold mb-2 flex items-center gap-3">
                <Info className="w-7 h-7 text-blue-500" />
                About
              </h2>
              <p className="text-sm text-gray-400">Device information and version</p>
            </div>

            <div className="flex-1 overflow-y-auto px-6 py-6">
              {/* Device Info */}
              <div className="mb-6 p-5 bg-gray-900 rounded-lg">
                <h3 className="text-lg font-semibold mb-4">Grateful Dead Concert Player</h3>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-400">Version:</span>
                    <span className="text-white">1.0.0</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">Build:</span>
                    <span className="text-white">2025.12.15</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">Shows Available:</span>
                    <span className="text-white">15,247</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">Source:</span>
                    <span className="text-white">Internet Archive</span>
                  </div>
                </div>
              </div>

              {/* Planned Features */}
              <div className="mb-6">
                <h3 className="text-lg font-semibold mb-3 text-gray-400">Planned Features</h3>
                <div className="space-y-2">
                  <div className="p-4 bg-gray-900 rounded-lg">
                    <div className="flex items-start gap-3">
                      <span className="text-2xl">🎤</span>
                      <div>
                        <div className="font-semibold mb-1">Voice Search</div>
                        <div className="text-sm text-gray-400">
                          Hands-free show discovery with natural language
                        </div>
                      </div>
                    </div>
                  </div>

                  <div className="p-4 bg-gray-900 rounded-lg">
                    <div className="flex items-start gap-3">
                      <span className="text-2xl">⏱️</span>
                      <div>
                        <div className="font-semibold mb-1">Sleep Timer</div>
                        <div className="text-sm text-gray-400">
                          Auto-stop playback after set duration
                        </div>
                      </div>
                    </div>
                  </div>

                  <div className="p-4 bg-gray-900 rounded-lg">
                    <div className="flex items-start gap-3">
                      <span className="text-2xl">📝</span>
                      <div>
                        <div className="font-semibold mb-1">Show Notes</div>
                        <div className="text-sm text-gray-400">
                          Add personal annotations and favorite moments
                        </div>
                      </div>
                    </div>
                  </div>

                  <div className="p-4 bg-gray-900 rounded-lg">
                    <div className="flex items-start gap-3">
                      <span className="text-2xl">🔄</span>
                      <div>
                        <div className="font-semibold mb-1">Recently Played</div>
                        <div className="text-sm text-gray-400">
                          Quick access to your listening history
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Credits */}
              <div className="p-5 bg-gray-900 rounded-lg">
                <h3 className="text-lg font-semibold mb-3">Credits</h3>
                <div className="text-sm text-gray-400 space-y-2">
                  <p>Built with ❤️ for Deadheads everywhere</p>
                  <p>Concert recordings courtesy of the Internet Archive</p>
                  <p>Thanks to all the tapers who preserved these moments</p>
                  <p className="text-xs pt-2 text-gray-600">⚡💀🌹</p>
                </div>
              </div>
            </div>
          </>
        ) : null}

        {/* Back Button */}
        <div className="border-t border-gray-800 p-6">
          <button 
            onClick={() => setCurrentView('browse')}
            className="w-full py-4 bg-gray-800 hover:bg-gray-700 rounded-lg font-semibold text-lg transition-colors"
          >
            ← Back to Browse
          </button>
        </div>
      </div>
    </div>
  );

  return (
    <div className="w-full h-screen bg-black">
      {currentView === 'player' ? <PlayerScreen /> : currentView === 'settings' ? <SettingsScreen /> : <BrowseScreen />}
    </div>
  );
};

export default DeadheadPlayerLandscape;
