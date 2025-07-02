// src/app/about/components/AboutCharts.tsx
'use client'; // This directive marks the component as a Client Component

import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

// Sample data for the chart
const data = [
  { name: 'Jan', 'Projects Completed': 40, 'User Growth': 2400 },
  { name: 'Feb', 'Projects Completed': 30, 'User Growth': 1398 },
  { name: 'Mar', 'Projects Completed': 20, 'User Growth': 9800 },
  { name: 'Apr', 'Projects Completed': 27, 'User Growth': 3908 },
  { name: 'May', 'Projects Completed': 18, 'User Growth': 4800 },
  { name: 'Jun', 'Projects Completed': 23, 'User Growth': 3800 },
  { name: 'Jul', 'Projects Completed': 34, 'User Growth': 4300 },
];

const AboutCharts = () => {
  return (
    <div className="bg-white p-6 rounded-lg shadow-md mt-6">
      <h3 className="text-2xl font-semibold text-gray-800 mb-4 text-left">Annual Overview</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart
          data={data}
          margin={{
            top: 5,
            right: 30,
            left: 20,
            bottom: 5,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="Projects Completed" stroke="#8884d8" activeDot={{ r: 8 }} />
          <Line type="monotone" dataKey="User Growth" stroke="#82ca9d" />
        </LineChart>
      </ResponsiveContainer>
      <p className="text-center text-sm text-gray-500 mt-4">
        Data represents hypothetical project completion and user growth metrics.
      </p>
    </div>
  );
};

export default AboutCharts;