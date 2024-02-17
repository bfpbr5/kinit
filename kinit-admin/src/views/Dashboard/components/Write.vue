<script setup lang="tsx">
import { Form, FormSchema } from '@/components/Form'
import { useForm } from '@/hooks/web/useForm'
import { reactive } from 'vue'
import { useValidator } from '@/hooks/web/useValidator'

const { required } = useValidator()

const formSchema = reactive<FormSchema[]>([
  {
    field: 'name',
    label: '案件名',
    component: 'Input',
    colProps: {
      span: 24
    }
  },
  {
    field: 'case_datetime',
    label: '案件日期',
    component: 'DatePicker',
    colProps: {
      span: 24
    },
    componentProps: {
      style: {
        width: '100%'
      },
      type: 'date',
      format: 'YYYY-MM-DD',
      valueFormat: 'YYYY-MM-DD'
    }
  }
])

const rules = reactive({
  name: [required()],
  case_datetime: [required()]
})

const { formRegister, formMethods } = useForm()
const { getFormData, getElFormExpose } = formMethods

const submit = async () => {
  const elForm = await getElFormExpose()
  const valid = await elForm?.validate()
  if (valid) {
    const formData = await getFormData()
    return formData
  }
}

defineExpose({
  submit
})
</script>

<template>
  <Form :rules="rules" @register="formRegister" :schema="formSchema" :labelWidth="90" />
</template>
