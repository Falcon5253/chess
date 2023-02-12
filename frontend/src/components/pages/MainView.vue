<template>
    <ul class='games-list'>
        <li class='games-list__item' v-for="game, index in games" :key="game.id">
            <p class='games-list__text'>{{ game.player1 }} против {{ game.player2 }}</p>
            <input type="button" value='К игре' @click='selectGame(game.id, index)'>
        </li>
    </ul>
</template>

<script>

export default {
    name: 'MainView',
    computed: {
        games() {
            // If game id in route, setting current game
            if (!isNaN(parseInt(this.$route.params.id))) {
                // Setting current game
                const id = this.$route.params.id;
                this.$store.dispatch('SET_CURRENT_GAME', id);

                // Subscribing to pusher
                let channel = this.$pusher.subscribe('game' + id);
                channel.bind('turnWasMade', (game) => {
                    this.$store.dispatch('UPDATE_GAME', game);
                });
            }

            return this.$store.getters.games;
        }
    },
    methods: {
        selectGame(gameId) {
            // Checking if current game is the game that is being pushed
            if (this.$route.params.id != gameId) {
                // Unsetting pusher and setting route
                let previousId = this.$route.params.id;
                this.$pusher.unsubscribe('game' + previousId);
                this.$router.push("/" + gameId);
            }

            // Showing the selected game
            this.$root.$emit('showGame', gameId);

            // Subscribing to pusher
            let channel = this.$pusher.subscribe('game' + this.gameId);
            channel.bind('turnWasMade', (game) => {
                this.$store.dispatch('UPDATE_GAME', game);
            });
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