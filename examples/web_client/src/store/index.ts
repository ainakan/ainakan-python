import Vue from 'vue';
import Vuex from 'vuex';

import ainakan from './modules/ainakan';
import ainakanBus from './plugins/ainakan';

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    ainakan
  },
  plugins: [
    ainakanBus()
  ]
});
