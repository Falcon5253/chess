<template>
    <ul class='games-list'>
        <li class='games-list__item' v-for="game in games" :key="game.id">
            <p class='games-list__text'>{{ game.player1 }} против {{ game.player2 }}</p>
            <input type="button" value='К игре' @click='selectGame()'>
        </li>
    </ul>
</template>

<script>

export default {
    name: 'MainView',
    computed: {
        games() {
            return this.$store.getters.games;
        }
    },
    methods: {
        // функция должна будет принимать id и находить нужную игру по нему для преобразования данных
        selectGame() {
            this.$root.$emit('showGame');
        }
    },
    mounted() {
        this.$store.dispatch('GET_GAMES');
    },
}

</script>

<style lang='scss'>

.games-list {
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