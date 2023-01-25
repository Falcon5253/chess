<template>
    <div v-if='isAuthenticated'>
        Все норм
    </div>
    <div v-else>
        Вы не авторизированы :(
    </div>
</template>

<script>

export default {
    name: 'MainView',
    computed: {
        isAuthenticated() {
            return this.$store.getters.isAuthenticated;
        }
    },
}

</script>