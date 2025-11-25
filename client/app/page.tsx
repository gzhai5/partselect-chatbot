/* eslint-disable @next/next/no-img-element */
import React from 'react';
import Navbar from './components/navbar/navbar';
import { ChatWidget } from './components/chat/chatWidget';

export default function Home() {
  return (
    <div className='bg-slate-200 h-screen gap-6 flex flex-col'>
        <Navbar />

        <div className="h-auto bg-slate-200 text-primary flex flex-col items-center">

            {/* Title Section */}
            <h1 className="text-5xl sm:text-5xl md:text-7xl mt-4 font-bold text-teal-800">Ready when you are.</h1>
            <p className="text-2xl sm:text-xl md:text-4xl mt-4 mb-6 font-semibold text-teal-800">Ask me about refrigerator or dishwasher!</p>

            {/* Chat Widget spanning across page */}
            <div className="w-5/6 max-w-[110rem] flex-1 flex">
                <ChatWidget />
            </div>
        </div>
    </div>
)
}
