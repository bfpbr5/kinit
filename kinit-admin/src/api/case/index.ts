import request from '@/config/axios'

export const PostCaseAnalysis = (dataId: number, data: any): Promise<IResponse> => {
  return request.post({ url: `/case/analysis/${dataId}`, data })
}

export const PostExplainAnalysis = (dataId: number, data: any): Promise<IResponse> => {
  return request.post({ url: `/case/explain/analysis/${dataId}`, data })
}

export const PostVerifyAnalysis = (dataId: number, data: any): Promise<IResponse> => {
  return request.post({ url: `/case/verify/analysis/${dataId}`, data })
}

export const PostChainOfEvidenceAnalysis = (dataId: number): Promise<IResponse> => {
  return request.post({ url: `/case/chain/of/evidence/generate/${dataId}` })
}

export const PostCreateCase = (data: any): Promise<IResponse> => {
  return request.post({ url: '/case/create', data })
}
