import React, { useEffect, useState } from 'react';
import Cookies from 'js-cookie';

function UserPanel() {
  const [user, setUser] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchUser() {
      try {
        // Lấy token từ cookie
        const authToken = Cookies.get('authToken');
        if (!authToken) {
          throw new Error('Authentication token not found in cookie.');
        }

        // Thực hiện yêu cầu fetch với token trong header Authorization
        const response = await fetch('http://localhost:8000/api/panel/me/', {
          method: 'POST',
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${authToken}`, // Đảm bảo token được tiền tố bằng 'Bearer'
          },
          body: JSON.stringify({ token: authToken })
        });

        if (response.ok) {
          const data = await response.json();
          setUser(data);
        } else {
          throw new Error('Failed to fetch user');
        }
      } catch (error) {
        // Xóa cookie nếu không thể truy xuất thông tin người dùng
        Cookies.remove('authToken');
        setError(error.message);
      }
    }

    fetchUser();
  }, []);

  if (error) {
    return (
      <div className="max-w-4xl mx-auto mt-8 p-6 bg-white shadow-md rounded-lg">
        <h2 className="text-2xl font-bold mb-6">Failed to fetch user data. Please login first.</h2>
      </div>
    );
  }

  if (!user) {
    return <div>Loading...</div>;
  }

  // Khi dữ liệu người dùng được truy xuất và không có lỗi, hiển thị giao diện người dùng
  return (
    <div className="max-w-4xl mx-auto mt-8 p-6 bg-white shadow-md rounded-lg">
      <h2 className="text-2xl font-bold mb-6">User Panel</h2>
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Email</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Username</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Display Name</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          <tr>
            <td className="px-6 py-4 whitespace-nowrap">{user.email}</td>
            <td className="px-6 py-4 whitespace-nowrap">{user.username}</td>
            <td className="px-6 py-4 whitespace-nowrap">{user.display_name}</td>
            <td className="px-6 py-4 whitespace-nowrap">{user.uid}</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}

export default UserPanel;
