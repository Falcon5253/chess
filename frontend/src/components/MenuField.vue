<template>
    <div class='menu-view'>
        <nav>
            <ul v-if='!isAuthenticated' class='navigation'>
                <li>
                    <router-link to="/login">Login</router-link>
                </li>
                <li>
                    <router-link to="/register">Register</router-link>
                </li>
            </ul>
            <ul v-else class='navigation'>
                <li>
                    <router-link to="/">Main</router-link>
                </li>
                <li>
                    <router-link to="/">Another link</router-link>
                </li>
                <li>
                    <router-link to="/">More links</router-link>
                </li>
                <li>
                    <router-link to="/login" @click.native='logout()'>Logout</router-link>
                </li>
            </ul>
        </nav>
        <router-view></router-view>
    </div>
</template>

<script>

import Cookies from 'js-cookie'

export default {
  name: 'MenuView',

  computed: {
    isAuthenticated() {
        return this.$store.getters.isAuthenticated;
    }
  },
  methods: {

    checkLogin() {
        fetch(this.$api + 'view/', {
            method: 'get',
            headers: {
                'Authorization': `Bearer ${this.$store.getters.token}` 
            },
        })
        .then((res) => res.json())
        .then((data) => {
            console.log(data);
        })
        .catch((err) => {
            console.log(err);
        })
    },
    logout() {
        fetch( this.$api + 'logout/', {
            method: 'post',
            headers: {
                'Authorization': `Bearer ${this.$store.getters.token}`
            },
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

        })
        .catch((err) => {
            console.log(err)
        })
        .finally(() => {
            Cookies.remove('token');
            this.$store.dispatch('TOGGLE_IS_AUTHENTICATED');
        })
    }
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

.navigation {
    display: flex;
    gap: 10px;
    list-style-type: none;
    a {
        display: block;
        background-color: black;
        color: white;
        font-weight: 600;
        text-decoration: none;
        padding: 10px;
    }
    a:hover {
        cursor: pointer;
        color: grey;
    }
}

</style>