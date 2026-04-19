"use client";

import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { Compass, Calendar, MapPin, Search, Navigation, DollarSign, Hotel, Link as LinkIcon, Loader2, Plane } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { postJson, API_BASE_URL } from '@/lib/api';

// Types
type TripRequest = {
  destination: string;
  origin: string;
  num_days: number;
  travelers: number;
  preferences: string;
  travel_style: string;
  dates: string;
};

type ItineraryDay = {
  day: number;
  title: string;
  activities: string[];
};

type TripResponse = {
  itinerary: ItineraryDay[];
  trip_theme_summary: string;
  destination: string;
  duration_days: number;
  seasonality: { season_info?: any; note?: string };
  budget: {
    total_estimated_budget: number;
    currency: string;
    daily_per_person?: any;
  };
  places: Array<{ name: string; description: string; category: string; osm_url: string; google_maps_url: string }>;
  booking_links: Record<string, string>;
  error?: string;
};

async function postPlanTrip(data: TripRequest): Promise<TripResponse> {
  const json = await postJson('/api/plan-trip', data) as any;
  if (json.error) throw new Error(json.error);
  return json as TripResponse;
}

export default function PlannerClient() {
  const [formData, setFormData] = useState<TripRequest>({
    destination: '',
    origin: '',
    num_days: 7,
    travelers: 1,
    preferences: 'mid',
    travel_style: 'chill',
    dates: 'next month',
  });

  const mutation = useMutation({
    mutationFn: postPlanTrip,
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.destination) return;
    mutation.mutate(formData);
  };

  return (
    <div className="flex flex-col md:flex-row min-h-screen bg-slate-950 text-slate-100">
      {/* Left Panel: Inputs */}
      <div className="w-full md:w-1/3 lg:w-1/4 p-6 glass-panel border-r border-white/5 z-10 flex flex-col h-screen overflow-y-auto sticky top-0">
        <div className="flex items-center gap-2 mb-8 font-bold text-2xl text-cyan-400">
          <Compass /> VoyaGen
        </div>

        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className="block text-sm text-slate-400 mb-1">Destination</label>
            <div className="relative">
              <MapPin className="absolute left-3 top-2.5 w-5 h-5 text-slate-500" />
              <input 
                required
                type="text" 
                placeholder="e.g. Kyoto, Japan" 
                className="w-full pl-10 pr-4 py-2 bg-slate-900/50 border border-slate-700 rounded-xl focus:outline-none focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500"
                value={formData.destination}
                onChange={e => setFormData({...formData, destination: e.target.value})}
              />
            </div>
          </div>
          
          <div>
            <label className="block text-sm text-slate-400 mb-1">Origin (for flights)</label>
            <div className="relative">
              <Navigation className="absolute left-3 top-2.5 w-5 h-5 text-slate-500" />
              <input 
                type="text" 
                placeholder="e.g. New York, USA" 
                className="w-full pl-10 pr-4 py-2 bg-slate-900/50 border border-slate-700 rounded-xl focus:outline-none focus:border-cyan-500"
                value={formData.origin}
                onChange={e => setFormData({...formData, origin: e.target.value})}
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm text-slate-400 mb-1">Duration (days)</label>
              <input 
                min="1" max="30" type="number" 
                className="w-full px-4 py-2 bg-slate-900/50 border border-slate-700 rounded-xl focus:outline-none focus:border-cyan-500"
                value={formData.num_days}
                onChange={e => setFormData({...formData, num_days: parseInt(e.target.value) || 1})}
              />
            </div>
            <div>
              <label className="block text-sm text-slate-400 mb-1">Travelers</label>
              <input 
                min="1" max="20" type="number" 
                className="w-full px-4 py-2 bg-slate-900/50 border border-slate-700 rounded-xl focus:outline-none focus:border-cyan-500"
                value={formData.travelers}
                onChange={e => setFormData({...formData, travelers: parseInt(e.target.value) || 1})}
              />
            </div>
          </div>

          <div>
            <label className="block text-sm text-slate-400 mb-1">Travel Style</label>
            <select 
              className="w-full px-4 py-2 bg-slate-900/50 border border-slate-700 rounded-xl focus:outline-none focus:border-cyan-500 text-slate-100"
              value={formData.travel_style}
              onChange={e => setFormData({...formData, travel_style: e.target.value})}
            >
              <option value="chill">Chill & Relaxed</option>
              <option value="adventure">Action & Adventure</option>
              <option value="cultural">Culture & History</option>
              <option value="party">Nightlife & Party</option>
            </select>
          </div>

          <div>
            <label className="block text-sm text-slate-400 mb-1">Budget Preference</label>
            <select 
              className="w-full px-4 py-2 bg-slate-900/50 border border-slate-700 rounded-xl focus:outline-none focus:border-cyan-500 text-slate-100"
              value={formData.preferences}
              onChange={e => setFormData({...formData, preferences: e.target.value})}
            >
              <option value="budget">Backpacker / Budget</option>
              <option value="mid">Mid-range / Comfort</option>
              <option value="luxury">Luxury / High-end</option>
            </select>
          </div>

          <button 
            type="submit" 
            disabled={mutation.isPending}
            className="w-full mt-4 flex items-center justify-center gap-2 py-3 px-4 bg-gradient-to-r from-cyan-500 to-sky-500 hover:from-cyan-400 hover:to-sky-400 text-white rounded-xl font-bold transition-all disabled:opacity-50"
          >
            {mutation.isPending ? <Loader2 className="animate-spin" /> : <Search />}
            {mutation.isPending ? "Crafting Itinerary..." : "Generate Magic"}
          </button>
        </form>

        {process.env.NODE_ENV === "development" && (
          <div className="mt-8 p-4 text-xs text-slate-400 bg-slate-900/50 rounded-xl border border-slate-800">
            <div className="font-semibold mb-1 text-slate-300">Developer Diagnostics</div>
            <div className="mb-3 break-all">API Base: {API_BASE_URL}</div>
            <button 
              type="button"
              onClick={async () => {
                 try {
                   const res = await fetch(`${API_BASE_URL}/health`, { method: 'GET' });
                   const text = await res.text();
                   if (!res.ok) throw new Error(`Status ${res.status}: ${text.slice(0,100)}`);
                   alert(`Backend is reachable. Response: ${text.slice(0, 50)}`);
                 } catch (err: any) {
                   alert(`Test failed!\n${err.message || String(err)}`);
                 }
              }}
              className="w-full px-3 py-2 bg-slate-800 hover:bg-slate-700 rounded text-slate-200 transition-colors"
            >
              Test Backend Reachability
            </button>
          </div>
        )}
      </div>

      {/* Right Panel: Results */}
      <div className="flex-1 p-6 md:p-12 overflow-y-auto w-full relative">
        <AnimatePresence mode="wait">
          {!mutation.data && !mutation.isPending && !mutation.isError && (
            <motion.div 
              key="empty"
              initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
              className="h-full flex flex-col items-center justify-center text-slate-500"
            >
              <Compass className="w-24 h-24 mb-4 opacity-20" />
              <p className="text-xl">Your adventure awaits. Define it on the left.</p>
            </motion.div>
          )}

          {mutation.isPending && (
            <motion.div 
              key="loading"
              initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
              className="h-full flex flex-col items-center justify-center pt-24"
            >
              <div className="relative w-32 h-32 mb-8">
                <div className="absolute inset-0 rounded-full border-t-2 border-cyan-400 animate-spin" />
                <div className="absolute inset-4 rounded-full border-r-2 border-sky-400 animate-spin flex items-center justify-center">
                   <Plane className="text-cyan-200" />
                </div>
              </div>
              <h2 className="text-2xl font-semibold text-transparent bg-clip-text bg-gradient-to-r from-cyan-300 to-sky-300">
                Consulting sources & building plan...
              </h2>
            </motion.div>
          )}

          {mutation.isError && (
            <motion.div 
              key="error"
              initial={{ opacity: 0 }} animate={{ opacity: 1 }}
              className="p-6 bg-red-900/30 border border-red-500/50 rounded-2xl text-red-200"
            >
              <h3 className="font-bold text-xl mb-2">Something went wrong</h3>
              <p>{(mutation.error as Error).message}</p>
            </motion.div>
          )}

          {mutation.data && (
            <motion.div 
              key="results"
              initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
              className="max-w-5xl mx-auto space-y-8 pb-32"
            >
              {/* Header Card */}
              <div className="glass-panel p-8 rounded-3xl relative overflow-hidden">
                <div className="absolute top-0 right-0 w-64 h-64 bg-cyan-500/10 rounded-full blur-3xl -mr-20 -mt-20 pointer-events-none" />
                <h1 className="text-4xl md:text-5xl font-extrabold mb-2">{mutation.data.destination}</h1>
                <p className="text-xl text-sky-400 font-medium mb-6">{mutation.data.trip_theme_summary}</p>
                
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
                  <div className="flex items-center gap-3">
                     <Calendar className="text-cyan-500" />
                     <div>
                       <div className="text-sm text-slate-400">Duration</div>
                       <div className="font-semibold">{mutation.data.duration_days} Days</div>
                     </div>
                  </div>
                  <div className="flex items-center gap-3">
                     <DollarSign className="text-teal-500" />
                     <div>
                       <div className="text-sm text-slate-400">Estimated Total</div>
                       <div className="font-semibold">
                         {mutation.data.budget?.total_estimated_budget 
                           ? `${mutation.data.budget.total_estimated_budget} ${mutation.data.budget.currency}`
                           : 'TBD'
                         }
                        </div>
                     </div>
                  </div>
                  <div className="flex items-center gap-3">
                     <Hotel className="text-indigo-400" />
                     <div>
                       <div className="text-sm text-slate-400">Season Note</div>
                       <div className="font-semibold text-sm line-clamp-2" title={mutation.data.seasonality?.note}>
                         {mutation.data.seasonality?.note || 'Any time is good'}
                       </div>
                     </div>
                  </div>
                </div>
              </div>

               {/* Top Places & Booking Links Grid */}
               <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                  {/* Places */}
                  <div className="space-y-4">
                    <h3 className="text-2xl font-bold flex items-center gap-2"><MapPin/> Key Places</h3>
                    <div className="grid grid-cols-1 gap-4">
                      {mutation.data.places?.map((p, i) => (
                        <div key={i} className="bg-slate-900/60 p-4 rounded-2xl border border-slate-800 hover:border-slate-700 transition-colors">
                          <div className="flex justify-between items-start mb-2">
                            <h4 className="font-bold text-lg text-cyan-50">{p.name}</h4>
                            <span className="text-xs px-2 py-1 bg-slate-800 rounded-full text-slate-300">{p.category}</span>
                          </div>
                          <p className="text-sm text-slate-400 mb-4">{p.description}</p>
                          <div className="flex gap-3">
                            <a target="_blank" rel="noreferrer" href={p.osm_url} className="text-xs text-sky-400 hover:text-sky-300 flex items-center gap-1">
                              <MapPin size={14}/> OSM Map
                            </a>
                            <a target="_blank" rel="noreferrer" href={p.google_maps_url} className="text-xs text-emerald-400 hover:text-emerald-300 flex items-center gap-1">
                              <MapPin size={14}/> G-Maps Search
                            </a>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Booking Link / Budget */}
                  <div className="space-y-8">
                    <div className="glass-panel p-6 rounded-2xl">
                       <h3 className="text-xl font-bold mb-4 flex items-center gap-2"><LinkIcon/> Check Tickets</h3>
                       <p className="text-sm text-slate-400 mb-4">Deep links to check live availability without using paid APIs.</p>
                       <div className="space-y-3 flex flex-col">
                          {Object.entries(mutation.data.booking_links || {}).map(([key, link]) => (
                            <a key={key} href={link} target="_blank" rel="noreferrer" 
                               className="px-4 py-3 bg-slate-800 hover:bg-slate-700 rounded-xl transition-colors text-sm font-medium flex justify-between items-center group">
                              <span className="capitalize">{key.replace('_', ' ')}</span>
                              <span className="text-cyan-400 group-hover:translate-x-1 transition-transform">→</span>
                            </a>
                          ))}
                       </div>
                    </div>

                    <div className="glass-panel p-6 rounded-2xl">
                       <h3 className="text-xl font-bold mb-4 flex items-center gap-2"><DollarSign/> Per Person Daily</h3>
                       <div className="space-y-3 text-sm">
                          <div className="flex justify-between border-b border-slate-800 pb-2">
                            <span className="text-slate-400">Hotel/Night</span>
                            <span className="font-bold">{mutation.data.budget?.daily_per_person?.hotel_per_night} {mutation.data.budget?.currency}</span>
                          </div>
                          <div className="flex justify-between border-b border-slate-800 pb-2">
                            <span className="text-slate-400">Food</span>
                            <span className="font-bold">{mutation.data.budget?.daily_per_person?.food} {mutation.data.budget?.currency}</span>
                          </div>
                          <div className="flex justify-between border-b border-slate-800 pb-2">
                            <span className="text-slate-400">Transport</span>
                            <span className="font-bold">{mutation.data.budget?.daily_per_person?.transport} {mutation.data.budget?.currency}</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-slate-400">Activities</span>
                            <span className="font-bold">{mutation.data.budget?.daily_per_person?.activities} {mutation.data.budget?.currency}</span>
                          </div>
                       </div>
                    </div>
                  </div>
               </div>

               {/* Itinerary */}
               <div className="mt-12">
                  <h3 className="text-3xl font-bold mb-8">Itinerary Plan</h3>
                  <div className="space-y-6">
                    {mutation.data.itinerary?.map((day, i) => (
                      <div key={i} className="glass-panel p-6 md:p-8 rounded-3xl relative overflow-hidden group">
                         <div className="absolute left-0 top-0 bottom-0 w-2 bg-gradient-to-b from-cyan-500 to-sky-500" />
                         <div className="flex flex-col md:flex-row md:items-center gap-4 mb-6">
                           <div className="bg-slate-800/50 px-4 py-2 rounded-xl text-cyan-400 font-bold whitespace-nowrap">
                             Day {day.day}
                           </div>
                           <h4 className="text-2xl font-bold">{day.title}</h4>
                         </div>
                         <ul className="space-y-3">
                           {day.activities.map((act, j) => (
                             <li key={j} className="flex gap-3 text-slate-300">
                               <span className="text-cyan-500 mt-1">•</span>
                               <span>{act}</span>
                             </li>
                           ))}
                         </ul>
                      </div>
                    ))}
                  </div>
               </div>

            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}
