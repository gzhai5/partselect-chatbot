import axios from "axios";
import swal from 'sweetalert';

const baseMcpUrl = `${process.env.NEXT_PUBLIC_MCP_BACKEND}`;

export const mcpInstance = axios.create({
    baseURL: baseMcpUrl,
    headers: {
        'Content-Type': 'application/json',
    },
});

mcpInstance.interceptors.response.use((response) => response, (error) => {
  swal({
    title: '',
    text: error.response?.data.detail,
    icon: 'error'
  });
  throw error.response?.data.detail;
});