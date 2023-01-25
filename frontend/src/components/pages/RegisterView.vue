<template>
    <div>
        <form id='login-form' class='login-form'>
            <label style='text-align: left' for='username'>Псевдоним</label>
            <input v-model='username' id='username' type="text" name='username' autocomplete='current-name'>
            <label style='text-align: left' for='email'>Почта</label>
            <input v-model='email' id='email' type="email" name='email' autocomplete='current-email'>
            <label style='text-align: left' for='password'>Пароль</label>
            <input v-model='password' id='password' type="password" name='password' autocomplete='current-password'>
            <input type="button" @click='tryRegister()' value='Зарегистрироваться'>
        </form>
    </div>
</template>

<script>

export default {
    name: 'RegisterView',
    data() {
        return {
            email: '',
            password: '',
            username: '',
        }
    },
    methods: {
        tryRegister() {
            const form = document.getElementById("login-form");
            const formData = new FormData(form);
            fetch(this.$api + 'register/', {
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
            .then(() => {
                this.email = '';
                this.password = '';
                this.$router.push('/register/success')
            })
            .catch((err) => {
                console.log(err);
            })
        },
    }
}

</script>