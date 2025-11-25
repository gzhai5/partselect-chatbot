import React from "react";
import { Ellipsis } from 'lucide-react';


export default function Navbar() {

    return (
        <div className="navbar bg-[#F3C04C] shadow-sm justify-end px-6">
            
            <div className="flex-none">
                <button className="btn btn-square btn-ghost">
                    <Ellipsis className="inline-block h-5 w-5 stroke-current" />
                </button>
            </div>
        </div>
    )
}