methods: {
    login() {
        axios.post('/login', data)
            .then(response => {
                if (response.data.status !== 'success') {
                    alert('登录失败');
                } else {
                    // 登录成功处理
                }
            })
            .catch(error => {
                console.error(error);
                alert('登录失败');
            });
    }
}