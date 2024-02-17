import { defineStore } from 'pinia'
import { store } from '../index'

interface CaseState {
  chainOfEvidenceDatas: any[]
  caseId: number
}

export const useCaseStore = defineStore('case', {
  state: (): CaseState => {
    return {
      chainOfEvidenceDatas: [],
      caseId: 0
    }
  },
  getters: {
    getChainOfEvidenceDatas(): any[] {
      return this.chainOfEvidenceDatas
    },
    getCaseId(): number {
      return this.caseId
    }
  },
  actions: {
    setChainOfEvidenceDatas(chainOfEvidenceDatas: any[]) {
      this.chainOfEvidenceDatas = chainOfEvidenceDatas
    },
    updateChainOfEvidenceUploadStatus(dataId: number) {
      const newData = this.chainOfEvidenceDatas.filter((item) => item.id === dataId)
      newData.map((item) => (item.upload_status = true))
    },
    setCaseId(caseId: number) {
      this.caseId = caseId
    }
  },
  persist: false
})

export const useCaseStoreWithOut = () => {
  return useCaseStore(store)
}
