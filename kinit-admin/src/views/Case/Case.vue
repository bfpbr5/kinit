<script setup lang="tsx">
import { ElTabs, ElTabPane } from 'element-plus'
import { ref } from 'vue'
import { ContentWrap } from '@/components/ContentWrap'
import AnalysisWrite from './components/AnalysisWrite.vue'
import ChainOfEvidenceWrite from './components/ChainOfEvidenceWrite.vue'

defineOptions({
  name: 'CaseCase'
})

const activeName = ref('analysis')

const toChainOfEvidence = () => {
  activeName.value = 'chainOfEvidence'
}
</script>

<template>
  <ContentWrap>
    <ElTabs v-model="activeName">
      <ElTabPane label="案例分析" name="analysis">
        <AnalysisWrite @to-chain-of-evidence="toChainOfEvidence" />
      </ElTabPane>
      <ElTabPane label="证据链生成" name="chainOfEvidence">
        <ChainOfEvidenceWrite />
      </ElTabPane>
    </ElTabs>
  </ContentWrap>
</template>
