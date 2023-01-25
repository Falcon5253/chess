<template>
    <div>
        <form id='login-form' class='login-form'>
            <label style='text-align: left' for='email'>Почта</label>
            <input v-model='email' id='email' type="email" name='email' autocomplete='current-email'>
            <label style='text-align: left' for='password'>Пароль</label>
            <input v-model='password' id='password' type="password" name='password' autocomplete='current-password'>
            <input type="button" @click='tryLogin()' value='Войти'>
        </form>
    </div>
</template>

<script>

import Cookies from 'js-cookie'


export default {
    name: 'LoginView',
    data() {
        return {
            email: '',
            password: '',
        }
    },
    methods: {
        tryLogin() {
            const form = document.getElementById("login-form");
            const formData = new FormData(form);
            fetch(this.$api + 'obtain-token/', {
                method: 'post',
                body: formData,
            })
            .then((res) => {
                if (res.ok) {
                    return res.json();
                }
                else {
                    throw new Error("Not 2xx response", {cause: res});
                }
            })
            .then((data) => {
                this.email = '';
                this.password = '';
                Cookies.set('token', data.token, { expires: 30 });
                this.$store.dispatch('SET_TOKEN', data.token);
                this.$store.dispatch('TOGGLE_IS_AUTHENTICATED');
                this.$router.push('/')
            })
            .catch((err) => {
                console.log(err);
            })
        },
    }
}

</script>