/* eslint-disable @next/next/no-img-element */
import React from 'react';
import Navbar from './components/navbar/navbar';
import { ChatWidget } from './components/chat/chatWidget';

export default function Home() {
  return (
    <div className='bg-[#939C62] min-h-screen gap-6 flex flex-col'>
        <Navbar />

        <div className="min-h-screen bg-[#939C62] text-primary flex flex-col items-center">

            {/* Title Section */}
            <h1 className="text-5xl mt-4 font-bold text-white">Ready when you are.</h1>
            <p className="text-xl mt-4 mb-6 font-semibold text-white">Ask me about refrigerator or dishwasher!</p>

            {/* Chat Widget spanning across page */}
            <div className="w-3/4 max-w-4xl">
                <ChatWidget />
            </div>
        </div>
    </div>
)
}
