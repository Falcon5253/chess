<template>
    <ul class='friends-list'>
        <li class='friends-list__item'>
            <p class='friends-list__text'>Вася</p>
            <router-link class='friends-list__link' to='/friends'>Бросить вызов</router-link>
            <router-link class='friends-list__link' to='/friends'>Перейти в чат</router-link>
        </li>
    </ul>
</template>

<script>

export default {
    name: 'FriendList',
}

</script>

<style lang='scss'>

.friends-list {
    list-style-type: none;
    padding-left: 0;
    &__item {
        
        background-color: grey;
        text-align: left;
        display: flex;
    }
    &__text {
        flex-grow: 1;
    }
    &__link {
        flex-shrink: 1;
    }
    &__text, &__link {
        margin: 10px;
    }
}

</style>