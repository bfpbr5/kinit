<script setup lang="tsx">
import {
  ElForm,
  ElFormItem,
  ElInput,
  ElRow,
  ElCol,
  ElPopover,
  ElUpload,
  UploadProps,
  ElMessage
} from 'element-plus'
import { ref, computed } from 'vue'
import {
  PostCaseAnalysis,
  PostExplainAnalysis,
  PostVerifyAnalysis,
  PostChainOfEvidenceAnalysis
} from '@/api/case'
// import { MarkdownViewer } from '@/components/MarkdownViewer'
import MarkdownIt from 'markdown-it'
import { useCaseStore } from '@/store/modules/case'
import { Dialog } from '@/components/Dialog'
import { useAuthStore } from '@/store/modules/auth'

const emit = defineEmits(['toChainOfEvidence'])

const caseStore = useCaseStore()
const authStore = useAuthStore()

const token = computed(() => authStore.getToken)
const caseId = computed(() => caseStore.getCaseId)

const dialogVisible = ref(false)
const explainContent = ref('')
const explain = async (textToVerify) => {
  const res = await PostExplainAnalysis(caseId.value, textToVerify)
  if (res) {
    const md = new MarkdownIt()
    explainContent.value = md.render(res.data)
  }
}

const verifyContent = ref('')
const verify = async (textToVerify) => {
  const res = await PostVerifyAnalysis(caseId.value, textToVerify)
  if (res) {
    const md = new MarkdownIt()
    verifyContent.value = md.render(res.data)
  }
}

const data = ref({
  cause: '',
  claim: '',
  questions: '',
  relation: '',
  timeline: ''
})

const caseContent = ref('')
const CABtnloading = ref(false)

const upload = () => {}

const caseAnalysis = async () => {
  if (caseContent.value) {
    CABtnloading.value = true
    try {
      const fromData = caseContent.value
      const res = await PostCaseAnalysis(caseId.value, fromData)
      if (res) {
        data.value = res.data
        const md = new MarkdownIt()
        data.value.relation = md.render(res.data.relation)
      }
    } finally {
      CABtnloading.value = false
    }
  }
}

const COEBtnLoading = ref(false)
const ChainOfEvidenceGenerate = async () => {
  COEBtnLoading.value = true
  try {
    const res = await PostChainOfEvidenceAnalysis(caseId.value)
    if (res) {
      caseStore.setChainOfEvidenceDatas(res.data)
      emit('toChainOfEvidence')
    }
  } finally {
    COEBtnLoading.value = false
  }
}

const beforeFileUpload: UploadProps['beforeUpload'] = (rawFile) => {
  const isFILE = ['image/jpeg', 'application/pdf', 'image/png'].includes(rawFile.type)
  const isLtSize = rawFile.size / 1024 / 1024 < 10

  if (!isFILE) {
    ElMessage.error('上传文件必须是 JPG/PDF/PNG/ 格式!')
  }
  if (!isLtSize) {
    ElMessage.error('上传文件大小不能超过 10MB!')
  }
  return isFILE && isLtSize
}

const uploadStatus = ref(false)

// 上传成功的钩子函数
const handleUploadSuccess: UploadProps['onSuccess'] = (response) => {
  if (response.code === 200) {
    uploadStatus.value = true
  } else {
    ElMessage.error(response.message)
  }
}
</script>

<template>
  <ElForm label-position="top" label-width="100px" :model="data">
    <ElFormItem>
      <ElInput
        v-model="caseContent"
        :rows="5"
        type="textarea"
        placeholder="请输入案情质量与生成分析内容质量挂钩，请尽量详细与清晰"
      />
      <template #label>
        <div class="flex justify-between">
          <span class="font-bold"> 请输入案情描述 </span>
          <span class="cursor-pointer" @click="dialogVisible = true">
            <Icon :size="18" icon="ep:chat-dot-round" />
          </span>
        </div>
      </template>
    </ElFormItem>
    <div class="ml-20px mb-20px flex justify-end">
      <ElUpload
        :action="`/api/case/analysis/file/upload/to/local/${caseId}`"
        :show-file-list="false"
        :before-upload="beforeFileUpload"
        :on-success="handleUploadSuccess"
        accept="image/jpeg,application/pdf,image/png"
        name="file"
        :limit="1"
        :headers="{ Authorization: token }"
        :disabled="uploadStatus"
      >
        <BaseButton @click="upload">{{ uploadStatus ? '已上传' : '上传文件' }}</BaseButton>
      </ElUpload>
      <BaseButton @click="caseAnalysis" :loading="CABtnloading" class="ml-20px"
        >分析案情</BaseButton
      >
    </div>
    <div class="mb-20px">
      <div class="font-bold">案情研究</div>
      <p v-html="data.relation"></p>
      <!-- <MarkdownViewer :markdown-content="data.relation" /> -->
    </div>
    <ElRow :gutter="20" justify="space-between">
      <ElCol :xl="12" :lg="12" :md="12" :sm="12" :xs="12">
        <ElFormItem>
          <ElInput :model-value="data.cause" :rows="5" type="textarea" placeholder="请输入" />
          <template #label>
            <div class="flex justify-between">
              <span> 案由 </span>
              <span class="cursor-pointer" @click="dialogVisible = true">
                <Icon :size="18" icon="ep:chat-dot-round" />
              </span>
            </div>
          </template>
        </ElFormItem>
        <div class="ml-20px mb-20px text-right">
          <ElPopover
            placement="top"
            :width="800"
            popper-class="max-h-300px overflow-auto"
            trigger="click"
          >
            <template #reference>
              <BaseButton @click="explain(data.cause)">解释</BaseButton>
            </template>
            <p v-html="explainContent"></p>
          </ElPopover>
          <ElPopover
            placement="top"
            :width="800"
            popper-class="max-h-300px overflow-auto"
            trigger="click"
          >
            <template #reference>
              <BaseButton @click="verify(data.cause)">验证</BaseButton>
            </template>
            <p v-html="verifyContent"></p>
          </ElPopover>
        </div>
      </ElCol>
      <ElCol :xl="12" :lg="12" :md="12" :sm="12" :xs="12">
        <ElFormItem>
          <ElInput :model-value="data.claim" :rows="5" type="textarea" placeholder="请输入" />
          <template #label>
            <div class="flex justify-between">
              <span> 诉讼请求 </span>
              <span class="cursor-pointer" @click="dialogVisible = true">
                <Icon :size="18" icon="ep:chat-dot-round" />
              </span>
            </div>
          </template>
        </ElFormItem>
        <div class="ml-20px mb-20px text-right">
          <ElPopover
            placement="top"
            :width="800"
            popper-class="max-h-300px overflow-auto"
            trigger="click"
          >
            <template #reference>
              <BaseButton @click="explain(data.claim)">解释</BaseButton>
            </template>
            <p v-html="explainContent"></p>
          </ElPopover>
          <ElPopover
            placement="top"
            :width="800"
            popper-class="max-h-300px overflow-auto"
            trigger="click"
          >
            <template #reference>
              <BaseButton @click="verify(data.claim)">验证</BaseButton>
            </template>
            <p v-html="verifyContent"></p>
          </ElPopover>
        </div>
      </ElCol>
    </ElRow>
    <ElRow :gutter="20" justify="space-between">
      <ElCol :xl="12" :lg="12" :md="12" :sm="12" :xs="12">
        <ElFormItem>
          <ElInput :model-value="data.timeline" :rows="5" type="textarea" placeholder="请输入" />
          <template #label>
            <div class="flex justify-between">
              <span> 时间线 </span>
              <span class="cursor-pointer" @click="dialogVisible = true">
                <Icon :size="18" icon="ep:chat-dot-round" />
              </span>
            </div>
          </template>
        </ElFormItem>
        <div class="ml-20px mb-20px text-right">
          <ElPopover
            placement="top"
            :width="800"
            popper-class="max-h-300px overflow-auto"
            trigger="click"
          >
            <template #reference>
              <BaseButton @click="explain(data.timeline)">解释</BaseButton>
            </template>
            <p v-html="explainContent"></p>
          </ElPopover>
          <ElPopover
            placement="top"
            :width="800"
            popper-class="max-h-300px overflow-auto"
            trigger="click"
          >
            <template #reference>
              <BaseButton @click="verify(data.timeline)">验证</BaseButton>
            </template>
            <p v-html="verifyContent"></p>
          </ElPopover>
        </div>
      </ElCol>
      <ElCol :xl="12" :lg="12" :md="12" :sm="12" :xs="12">
        <ElFormItem>
          <ElInput :model-value="data.questions" :rows="5" type="textarea" placeholder="请输入" />
          <template #label>
            <div class="flex justify-between">
              <span> 待澄清问题 </span>
              <span class="cursor-pointer" @click="dialogVisible = true">
                <Icon :size="18" icon="ep:chat-dot-round" />
              </span>
            </div>
          </template>
        </ElFormItem>
        <div class="ml-20px mb-20px text-right">
          <ElPopover
            placement="top"
            :width="800"
            popper-class="max-h-300px overflow-auto"
            trigger="click"
          >
            <template #reference>
              <BaseButton @click="explain(data.questions)">解释</BaseButton>
            </template>
            <p v-html="explainContent"></p>
          </ElPopover>
          <ElPopover
            placement="top"
            :width="800"
            popper-class="max-h-300px overflow-auto"
            trigger="click"
          >
            <template #reference>
              <BaseButton @click="verify(data.questions)">验证</BaseButton>
            </template>
            <p v-html="verifyContent"></p>
          </ElPopover>
        </div>
      </ElCol>
    </ElRow>
    <div class="mt-50px text-center">
      <BaseButton @click="ChainOfEvidenceGenerate" :loading="COEBtnLoading">证据链生成</BaseButton>
    </div>
  </ElForm>

  <Dialog v-model="dialogVisible" title="对话框" :height="380" :width="550">
    <template #footer>
      <BaseButton type="primary"> 保存 </BaseButton>
      <BaseButton @click="dialogVisible = false">关闭</BaseButton>
    </template>
  </Dialog>
</template>
