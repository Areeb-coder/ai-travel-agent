"use client";

import { Canvas, useFrame } from '@react-three/fiber';
import { Sphere, MeshDistortMaterial, Stars } from '@react-three/drei';
import { useRef, useState, useEffect } from 'react';
import * as THREE from 'three';
import Link from 'next/link';
import { Plane, Compass } from 'lucide-react';
import { motion } from 'framer-motion';

function AnimatedGlobe() {
  const meshRef = useRef<THREE.Mesh>(null!);
  
  useFrame((state) => {
    if (meshRef.current) {
      meshRef.current.rotation.y = state.clock.getElapsedTime() * 0.2;
      meshRef.current.rotation.z = Math.sin(state.clock.getElapsedTime() * 0.1) * 0.1;
    }
  });

  return (
    <Sphere ref={meshRef} args={[1, 64, 64]} scale={2.5}>
      <MeshDistortMaterial
        color="#0ea5e9"
        attach="material"
        distort={0.15}
        speed={1.5}
        roughness={0.2}
        metalness={0.8}
        wireframe={true}
      />
    </Sphere>
  );
}

export default function Home() {
  const [clientReady, setClientReady] = useState(false);
  useEffect(() => {
    setClientReady(true);
  }, []);

  return (
    <div className="flex flex-col min-h-screen relative overflow-hidden">
      <div className="absolute inset-0 z-0 h-full w-full">
        {clientReady && (
          <Canvas camera={{ position: [0, 0, 5], fov: 45 }}>
            <ambientLight intensity={0.5} />
            <directionalLight position={[10, 10, 5]} intensity={1} />
            <Stars radius={100} depth={50} count={5000} factor={4} saturation={0} fade speed={1} />
            <AnimatedGlobe />
          </Canvas>
        )}
      </div>
      
      <div className="z-10 flex flex-col min-h-screen">
        <header className="p-6 flex justify-between items-center bg-slate-900/50 backdrop-blur-sm border-b border-white/5">
          <div className="flex items-center gap-2 text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-cyan-400 to-sky-500">
            <Compass className="text-cyan-400" />
            VoyaGen
          </div>
        </header>

        <main className="flex-grow flex items-center justify-center p-6">
          <div className="text-center max-w-3xl glass-panel p-12 rounded-3xl">
            <motion.h1 
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
              className="text-5xl md:text-7xl font-extrabold mb-6 tracking-tight"
            >
              The World, <br/>
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-sky-400 via-cyan-400 to-teal-400">
                Perfectly Curated.
              </span>
            </motion.h1>
            
            <motion.p 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.3, duration: 0.8 }}
              className="text-xl md:text-2xl text-slate-400 mb-10 max-w-2xl mx-auto"
            >
              AI-crafted itineraries that fit your exact budget, pace, and vibe. Research, map integration, and ticket discovery, ready in seconds.
            </motion.p>
            
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.6, duration: 0.5 }}
            >
              <Link 
                href="/plan" 
                className="inline-flex items-center gap-3 px-8 py-4 bg-gradient-to-r from-sky-500 to-cyan-500 hover:from-sky-400 hover:to-cyan-400 text-white rounded-full font-semibold text-lg shadow-[0_0_40px_rgba(14,165,233,0.4)] transition-all transform hover:scale-105"
              >
                <Plane className="w-6 h-6" />
                Plan Your Trip
              </Link>
            </motion.div>
          </div>
        </main>
      </div>
    </div>
  );
}
