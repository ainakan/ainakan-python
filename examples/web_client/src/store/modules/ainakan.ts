import { Module } from 'vuex';

interface AinakanState {
  processes: Process[],
}

type Process = [number, string];

const ainakanModule: Module<AinakanState, any> = {
  state: {
    processes: []
  },

  mutations: {
  }
};

export default ainakanModule;
