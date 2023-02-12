<template>
    <div class='game-view'>
        <div  class='board' :class="{ player2 : isPlayer2 }">
            <div class='figures'>
                <CellBlock
                    class='drop-field'
                    :class="{ player2 : isPlayer2 }"
                    v-for='cell, index in gameData' v-bind:key='cell.id'
                    :cell="cell"
                    :isTurnMade=isTurnMade
                    :waitingForOpponent='!isMyTurn'
                    :index=index
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
        <div
            :class="{ hidden : isMyTurn }">
            Ожидание хода опонента
        </div>
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
            isTurnMade: false,
            turn: '',
        }
    },
    computed: {
        
        game() {
            return this.$store.getters.getGame;
        },
        gameData() {
            if (this.game != undefined) {
                return this.game['game_data'];
            }
            return {}
        },
        gameId() {
            if (this.game != undefined) {
                return this.game['id'];
            }
            return -1
        },
        index() {
            return this.$store.getters.games.find(game => game == this.game);
        },
        isPlayer2() {
            if (this.game != undefined) {
                if (this.game.player2 == this.$store.getters.profile['email']) {
                    return true
                }
            }
            return false;
        },
        isMyTurn() {
            if (this.game != undefined) {
                if (this.game.player2 == this.game.whose_turn) {
                    return this.isPlayer2;
                }
                return !this.isPlayer2;
            }
            return false;
        }
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
            this.$store.dispatch('SEND_TURN', {'game_id': this.gameId, 'turn': this.turn});
            this.isTurnMade = false;
            this.waitingForOpponent = true;

            // Setting awaiting for opponent
            if (this.isPlayer2) {
                this.game.whose_turn = this.game.player1;
            }
            else {
                this.game.whose_turn = this.game.player2;
            }
        }
    },
    name: 'GameView',
    mounted() {
        // On showGame event setting current game
        this.$root.$on('showGame', (id) => {
            this.$store.dispatch('SET_CURRENT_GAME', id)
        });
    },
}
</script>

<style lang='scss'>

.game-view {
    width: 50%;
    user-select: none;
}

.showMessage

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

.hidden {
    display: none;
}

@media (max-width: 1280px) {
    .board { 
        width: 480px;
        height: 480px;
    }
    .figures {
        grid-template-columns: repeat(8, 60px);
    }
}

@media (max-width: 960px) {
    .board { 
        width: 320px;
        height: 320px;
    }
    .figures {
        grid-template-columns: repeat(8, 40px);
    }
}
</style>