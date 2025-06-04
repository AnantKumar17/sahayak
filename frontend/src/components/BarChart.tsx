// import { Bar } from 'react-chartjs-2';
// import { Chart as ChartJS, BarElement, CategoryScale, LinearScale, Tooltip, Legend } from 'chart.js';
// import { PastReview } from '../types';

// ChartJS.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend);

// interface Props {
//   reviews: PastReview[];
// }

// function BarChart({ reviews }: Props) {
//   const data = {
//     labels: reviews.map((_, index) => `Review ${index + 1}`),
//     datasets: [
//       {
//         label: 'Similarity (%)',
//         data: reviews.map((review) => review.similarity * 100),
//         backgroundColor: ['#005566', '#E6F0FA'],
//         borderColor: '#005566',
//         borderWidth: 1,
//       },
//     ],
//   };

//   const options = {
//     scales: {
//       y: {
//         beginAtZero: true,
//         max: 100,
//         title: {
//           display: true,
//           text: 'Similarity (%)',
//         },
//       },
//     },
//     plugins: {
//       legend: {
//         display: false,
//       },
//     },
//     maintainAspectRatio: false,
//   };

//   return (
//     <div className="bar-chart">
//       <h3>Similarity Distribution</h3>
//       <div style={{ height: '200px' }}>
//         <Bar data={data} options={options} />
//       </div>
//     </div>
//   );
// }

// export default BarChart;

import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, BarElement, CategoryScale, LinearScale, Tooltip, Legend } from 'chart.js';
import { PastReview } from '../types';

ChartJS.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend);

interface Props {
  reviews: PastReview[];
}

function BarChart({ reviews }: Props) {
  const data = {
    labels: reviews.map((_, index) => `Review ${index + 1}`),
    datasets: [
      {
        label: 'Similarity (%)',
        data: reviews.map((review) => review.similarity * 100),
        backgroundColor: ['#005566', '#4A8294'], // Changed second color
        borderColor: '#005566',
        borderWidth: 1,
      },
    ],
  };

  const options = {
    scales: {
      y: {
        beginAtZero: true,
        max: 100,
        title: {
          display: true,
          text: 'Similarity (%)',
        },
      },
    },
    plugins: {
      legend: {
        display: false,
      },
    },
    maintainAspectRatio: false,
  };

  return (
    <div className="bar-chart">
      <h3>Similarity Distribution</h3>
      <div style={{ height: '200px' }}>
        <Bar data={data} options={options} />
      </div>
    </div>
  );
}

export default BarChart;