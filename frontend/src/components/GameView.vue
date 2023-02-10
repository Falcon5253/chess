<template>
    <div class='game-view'>
        <div  class='board' :class="{ player2 : isPlayer2 }">
            <div class='figures'>
                <CellBlock
                    class='drop-field'
                    :class="{ player2 : isPlayer2 }"
                    v-for='cell, index in gameData' v-bind:key='cell.id'
                    :cell="cell"
                    :index=index
                    :isTurnMade=isTurnMade
                    @makeTurn="(e, data) => makeTurn(e, data)"
                ></CellBlock>
            </div>
            <img class="board-img" alt='board' src="@/assets/board.svg" draggable='false'>
        </div>
        <input
            class='commit-turn'
            type="button"
            value='Поддвердить ход'
            :disabled='!isTurnMade'
            @click='sendTurnData()'>
    </div>
</template>

<script>
import CellBlock from "@/components/blocks/CellBlock.vue"

export default {
    components: {
        CellBlock,
    },
    data() {
        return {
            gameId: -1,
            isTurnMade: false,
            turn: '',
        }
    },
    computed: {
        gameData() {
            if (this.gameId != -1 && this.game != undefined) {
                return this.game['game_data'];
            }
            return []
        },
        game() {
            return this.$store.getters.games.find(element => element.id == this.gameId);
        },
        isPlayer2() {
            if (this.game != undefined) {
                if (this.game.player2 == this.$store.getters.profile['email']) {
                    return true
                }
            }
            return false;
        },
    },
    methods: {
        makeTurn(data) {

            // Getting turn data
            data = data.split(",");
            let figure = data[0]
            let fromIndex = data[1]
            let toIndex = data[2]
            
            // Editing game data
            this.gameData[fromIndex].figure = 'empty';
            this.gameData[toIndex].figure = figure;
            
            // Creating turn for server request
            let from = this.gameData[fromIndex].cell;
            let to = this.gameData[toIndex].cell;
            this.turn = from + "-" + to;

            this.isTurnMade = true;           
        },
        sendTurnData() {
            this.$store.dispatch('SEND_TURN', {'game_id': this.gameId, 'turn': this.turn})
        }
    },
    name: 'GameView',
    mounted() {
        this.$root.$on('showGame', (gameId) => this.gameId = gameId);

        // Checking if gameId in path and getting it from there
        if (!isNaN(parseInt(this.$route.params.id))) {
            this.gameId = this.$route.params.id;
        }
    },
}
</script>

<style lang='scss'>

.game-view {
    width: 50%;
    user-select: none;
}

.dragging {
    opacity: 100%;
    cursor: pointer;
}

.player2 {
    transform: rotate(180deg);
}

.board {
    border: 2px solid;
    width: 640px;
    height: 640px;
    position: relative;
    margin-left: auto;
    margin-right: auto;
}
.board-img {
    width: 100%;
}

.figures {
    position: absolute;
    display: grid;
    width: 100%;
    height: 100%;
    grid-template-columns: repeat(8, 80px);
    img {
        width: 100%;
    }
}

.commit-turn {
    margin-top: 15px;
    width: 640px;    
    height: 60px;
}

.commit-turn:disabled {
    display: none;
}

@media (max-width: 1280px) {
    .board { 
        width: 480px;
        height: 480px;
    }
}

@media (max-width: 960px) {
    .board { 
        width: 320px;
        height: 320px;
    }
}
</style>