<template>
    <div class='menu-view'>
        <div v-if="isAuthenticated">
            Авторизован
        </div>
        <div v-else>
            <form id='login-form' class='login-form' action="">
                <label style='text-align: left' for='email'>Почта</label>
                <input v-model='email' id='email' type="email" name='email' autocomplete='current-email'>
                <label style='text-align: left' for='password'>Пароль</label>
                <input v-model='password' id='password' type="password" name='password' autocomplete='current-password'>
                <input type="submit">
                <input type="button" @click='tryLogin()' value='log in'>
                <input type="button" @click='checkLogin()' value='check auth'>
            </form>
        </div>
    </div>
</template>

<script>


function setCookie(cName, cValue, expDays) {
        let date = new Date();
        date.setTime(date.getTime() + (expDays * 24 * 60 * 60 * 1000));
        const expires = "expires=" + date.toUTCString();
        document.cookie = cName + "=" + cValue + "; " + expires + "; path=/";
}



export default {
  name: 'MenuView',
  data() {
    return {
        email: '',
        password: '',
    }
  },
  computed: {
    isAuthenticated() {
        return this.$store.getters.isAuthenticated;
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
        .then((res) => res.json())
        .then((data) => {
            setCookie('token', data.token, 30)
            this.$store.dispatch('SET_TOKEN', data.token)
        })
        .catch((err) => {
            console.log(err)
        })
    },
    checkLogin() {
        fetch( this.$api + 'view/', {
            method: 'get',
            headers: {
                'Authorization': `Bearer ${this.$store.getters.token}` 
            },
        })
        .then((res) => res.json())
        .then((data) => {
            console.log(data)
        })
        .catch((err) => {
            console.log(err)
        })
    },
  },
}

</script>

<style lang='scss'>

.menu-view {
    width: 50%;
}

.login-form {
    margin-left: auto;
    margin-right: auto;
    width: 300px;
    display: flex;
    flex-direction: column;
    gap: 5px;
}

</style>