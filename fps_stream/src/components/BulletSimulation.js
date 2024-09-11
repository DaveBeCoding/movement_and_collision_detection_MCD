import React, { useEffect, useRef, useState } from "react";

const BulletSimulation = () => {
  const canvasRef = useRef(null);
  const [ws, setWs] = useState(null);

  useEffect(() => {
    const websocket = new WebSocket("ws://localhost:8765");
    setWs(websocket);

    websocket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      drawSimulation(data);
    };

    return () => {
      websocket.close();
    };
  }, []);

  const drawSimulation = (data) => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");

    // Clear the canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw the target
    ctx.beginPath();
    ctx.arc(data.target_x, data.target_y, data.target_radius, 0, 2 * Math.PI);
    ctx.fillStyle = "blue";
    ctx.fill();

    // Draw the bullet
    ctx.beginPath();
    ctx.arc(data.bullet_x, data.bullet_y, 5, 0, 2 * Math.PI);
    ctx.fillStyle = "red";
    ctx.fill();
  };

  return <canvas ref={canvasRef} width={800} height={600}></canvas>;
};

export default BulletSimulation;
