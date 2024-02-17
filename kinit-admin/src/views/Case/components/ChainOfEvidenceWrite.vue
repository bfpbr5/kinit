<script setup lang="tsx">
import {
  ElForm,
  ElFormItem,
  ElInput,
  ElRow,
  ElCol,
  ElText,
  ElDropdown,
  ElDropdownMenu,
  ElDropdownItem,
  UploadProps,
  ElMessage,
  ElUpload,
  ElPopover
} from 'element-plus'
import { computed, ref } from 'vue'
import { Icon } from '@/components/Icon'
import { useCaseStore } from '@/store/modules/case'
import { useAuthStore } from '@/store/modules/auth'
import { PostExplainAnalysis, PostVerifyAnalysis } from '@/api/case'
import MarkdownIt from 'markdown-it'

const caseStore = useCaseStore()
const authStore = useAuthStore()

const token = computed(() => authStore.getToken)

const data = computed(() => caseStore.getChainOfEvidenceDatas)

const upload = () => {}
const deleteBtn = () => {}

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

// 上传成功的钩子函数
const handleUploadSuccess: UploadProps['onSuccess'] = (response) => {
  if (response.code === 200) {
    let data_id = response.data.data_id
    caseStore.updateChainOfEvidenceUploadStatus(data_id)
  } else {
    ElMessage.error(response.message)
  }
}

const explainContent = ref('')
const explain = async () => {
  const res = await PostExplainAnalysis()
  if (res) {
    const md = new MarkdownIt()
    explainContent.value = md.render(res.data)
  }
}

const verifyContent = ref('')
const verify = async () => {
  const res = await PostVerifyAnalysis()
  if (res) {
    const md = new MarkdownIt()
    verifyContent.value = md.render(res.data)
  }
}
</script>

<template>
  <ElForm label-position="top" label-width="100px" :model="data">
    <ElRow :gutter="20" justify="space-between">
      <template v-for="(item, index) in data" :key="index">
        <ElCol :span="12">
          <ElFormItem>
            <ElInput
              :model-value="item.content"
              disabled
              :rows="5"
              type="textarea"
              placeholder="请输入"
            />
            <template #label>
              <div class="flex justify-between">
                <span>
                  {{ '主要证据' + (index + 1).toString() }}
                </span>

                <ElDropdown trigger="click">
                  <span class="cursor-pointer">
                    <Icon :size="18" icon="ri:more-fill" />
                  </span>
                  <template #dropdown>
                    <ElDropdownMenu>
                      <ElDropdownItem>
                        <BaseButton @click="deleteBtn" link>删除</BaseButton>
                      </ElDropdownItem>
                    </ElDropdownMenu>
                  </template>
                </ElDropdown>
              </div>
            </template>
          </ElFormItem>
          <div class="flex justify-between">
            <div class="flex justify-between">
              <ElUpload
                :action="`/api/case/chain/of/evidence/file/upload/to/local/${item.id}`"
                :show-file-list="false"
                :before-upload="beforeFileUpload"
                :on-success="handleUploadSuccess"
                accept="image/jpeg,application/pdf,image/png"
                name="file"
                :limit="1"
                :headers="{ Authorization: token }"
                :disabled="item.upload_status"
              >
                <BaseButton @click="upload">{{
                  item.upload_status ? '已上传' : '点击上传'
                }}</BaseButton>
              </ElUpload>
              <div class="ml-10px">
                <ElPopover
                  placement="top"
                  :width="800"
                  popper-class="max-h-300px overflow-auto"
                  trigger="click"
                >
                  <template #reference>
                    <BaseButton @click="explain">证据分析</BaseButton>
                  </template>
                  <p v-html="explainContent"></p>
                </ElPopover>
              </div>
            </div>
            <div>
              <ElPopover
                placement="top"
                :width="800"
                popper-class="max-h-300px overflow-auto"
                trigger="click"
              >
                <template #reference>
                  <BaseButton @click="verify">解析</BaseButton>
                </template>
                <p v-html="verifyContent"></p>
              </ElPopover>
            </div>
          </div>
          <div class="mb-20px">
            <ElText type="info"> 只能上传png/jpg/pdf文件，且不超过10MB </ElText>
          </div>
        </ElCol>
      </template>
    </ElRow>
  </ElForm>
</template>
