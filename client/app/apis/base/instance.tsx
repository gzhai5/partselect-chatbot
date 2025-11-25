import axios from "axios";
import swal from 'sweetalert';

const baseURL = `${process.env.NEXT_PUBLIC_CHAT_BACKEND}`;

export const instance = axios.create({
    baseURL: baseURL,
    headers: {
        'Content-Type': 'application/json',
    },
});

instance.interceptors.response.use((response) => response, (error) => {
  swal({
    title: '',
    text: error.response?.data.detail,
    icon: 'error'
  });
  throw error.response?.data.detail;
});