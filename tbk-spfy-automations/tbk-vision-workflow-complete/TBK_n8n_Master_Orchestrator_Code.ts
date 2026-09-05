// TBK_Vision_Orchestrator - n8n Workflow (Deployable)
// Version: 1.0 | Production Ready
// This is the master orchestrator workflow using n8n SDK

import { 
  IWorkflowBase,
  INode,
  IConnection,
  NodeConnectionType,
} from "n8n-workflow";

export const workflow: IWorkflowBase = {
  name: "TBK_Vision_Orchestrator",
  nodes: [
    // ===== NODE 1: Webhook Trigger =====
    {
      name: "Webhook_Trigger",
      type: "n8n-nodes-base.webhook",
      typeVersion: 1,
      position: [240, 280],
      parameters: {
        path: "tbk-vision-batch-upload",
        method: "POST",
        httpMethod: "POST",
        responseMode: "responseNode",
        responseData: "autoRespond",
        authentication: "headerAuth",
        headerAuthorizationMethod: "Bearer"
      },
      credentials: {
        httpBasicAuth: "api_key_credential_id"
      }
    },

    // ===== NODE 2: Set Execution Variables =====
    {
      name: "Set_Execution_Context",
      type: "n8n-nodes-base.set",
      typeVersion: 3,
      position: [480, 280],
      parameters: {
        values: {
          string: [
            {
              name: "batch_id",
              value: "={{ $json.batch_id }}"
            },
            {
              name: "execution_id",
              value: "={{ $randomUUID() }}"
            },
            {
              name: "source",
              value: "={{ $json.source || 'api' }}"
            }
          ],
          number: [
            {
              name: "file_count",
              value: "={{ $json.file_urls.length }}"
            }
          ],
          bool: [
            {
              name: "debug_mode",
              value: false
            }
          ]
        },
        keepOnlySet: false
      },
      options: {}
    },

    // ===== NODE 3: Validate Input Schema =====
    {
      name: "Validate_Input_Schema",
      type: "n8n-nodes-base.code",
      typeVersion: 2,
      position: [720, 280],
      parameters: {
        language: "javaScript",
        jsCode: `
// Validate input payload
const batch_id = $json.batch_id;
const file_urls = $json.file_urls || [];

if (!batch_id || batch_id.trim().length === 0) {
  throw new Error("batch_id is required and must not be empty");
}

if (!Array.isArray(file_urls) || file_urls.length === 0) {
  throw new Error("file_urls must be a non-empty array");
}

if (file_urls.length > 1000) {
  throw new Error("Batch size exceeds 1000 images; split into smaller batches");
}

// Validate each URL format
file_urls.forEach((url, index) => {
  if (!url.startsWith("s3://") && !url.startsWith("http")) {
    throw new Error(\`Invalid URL at index \${index}: \${url}\`);
  }
});

return {
  batch_id,
  file_urls,
  file_count: file_urls.length,
  validated: true,
  timestamp: new Date().toISOString()
};
`
      }
    },

    // ===== NODE 4: PostgreSQL - Create Batch Record =====
    {
      name: "Create_Batch_Record",
      type: "n8n-nodes-base.postgres",
      typeVersion: 2,
      position: [960, 280],
      parameters: {
        operation: "executeQuery",
        query: `INSERT INTO batches 
          (batch_id, execution_id, source, file_count, status, created_at) 
          VALUES ($1, $2, $3, $4, 'processing', NOW())
          RETURNING batch_id, execution_id, created_at;`,
        queryParametersUi: {
          parameters: [
            {
              name: "$1",
              value: "={{ $node.Set_Execution_Context.json.batch_id }}"
            },
            {
              name: "$2",
              value: "={{ $node.Set_Execution_Context.json.execution_id }}"
            },
            {
              name: "$3",
              value: "={{ $node.Set_Execution_Context.json.source }}"
            },
            {
              name: "$4",
              value: "={{ $node.Set_Execution_Context.json.file_count }}"
            }
          ]
        }
      },
      credentials: {
        postgres: "postgres_tbk_credentials"
      }
    },

    // ===== NODE 5: Loop - For Each File (Parallel Sub-Workflows) =====
    {
      name: "Loop_Each_File",
      type: "n8n-nodes-base.itemLists",
      typeVersion: 3,
      position: [240, 420],
      parameters: {
        operation: "splitOutItems",
        splitInBatches: true,
        batchSize: 5  // Process 5 files at a time
      }
    },

    // ===== NODE 6: Call Input Validation Sub-Workflow =====
    {
      name: "Call_Input_Validation_WF",
      type: "n8n-nodes-base.executeWorkflow",
      typeVersion: 1,
      position: [480, 420],
      parameters: {
        workflowId: "{{ $env.TBK_INPUT_VALIDATION_WF_ID }}",
        waitForCompletion: true,
        workflowFieldsUi: {
          workflowFields: [
            {
              fieldName: "batch_id",
              fieldValue: "={{ $node.Set_Execution_Context.json.batch_id }}"
            },
            {
              fieldName: "file_url",
              fieldValue: "={{ $json.file_urls[$json.index] }}"
            },
            {
              fieldName: "source",
              fieldValue: "={{ $node.Set_Execution_Context.json.source }}"
            }
          ]
        }
      }
    },

    // ===== NODE 7: Call Qwen Vision Sub-Workflow =====
    {
      name: "Call_Qwen_Vision_WF",
      type: "n8n-nodes-base.executeWorkflow",
      typeVersion: 1,
      position: [720, 420],
      parameters: {
        workflowId: "{{ $env.TBK_QWEN_VISION_WF_ID }}",
        waitForCompletion: true,
        workflowFieldsUi: {
          workflowFields: [
            {
              fieldName: "image_id",
              fieldValue: "={{ $node.Call_Input_Validation_WF.json.validated[0].image_id }}"
            },
            {
              fieldName: "s3_path",
              fieldValue: "={{ $node.Call_Input_Validation_WF.json.validated[0].s3_path }}"
            },
            {
              fieldName: "batch_id",
              fieldValue: "={{ $node.Set_Execution_Context.json.batch_id }}"
            }
          ]
        }
      }
    },

    // ===== NODE 8: Call Genome Builder Sub-Workflow =====
    {
      name: "Call_Genome_Builder_WF",
      type: "n8n-nodes-base.executeWorkflow",
      typeVersion: 1,
      position: [960, 420],
      parameters: {
        workflowId: "{{ $env.TBK_GENOME_BUILDER_WF_ID }}",
        waitForCompletion: true,
        workflowFieldsUi: {
          workflowFields: [
            {
              fieldName: "vision_data",
              fieldValue: "={{ JSON.stringify($node.Call_Qwen_Vision_WF.json.vision_result) }}"
            },
            {
              fieldName: "image_id",
              fieldValue: "={{ $node.Call_Qwen_Vision_WF.json.image_id }}"
            },
            {
              fieldName: "confidence_scores",
              fieldValue: "={{ JSON.stringify($node.Call_Qwen_Vision_WF.json.confidence_scores) }}"
            }
          ]
        }
      }
    },

    // ===== NODE 9: Call SEO Generator Sub-Workflow =====
    {
      name: "Call_SEO_Generator_WF",
      type: "n8n-nodes-base.executeWorkflow",
      typeVersion: 1,
      position: [1200, 420],
      parameters: {
        workflowId: "{{ $env.TBK_SEO_GENERATOR_WF_ID }}",
        waitForCompletion: true,
        workflowFieldsUi: {
          workflowFields: [
            {
              fieldName: "genome",
              fieldValue: "={{ JSON.stringify($node.Call_Genome_Builder_WF.json.genome) }}"
            },
            {
              fieldName: "image_id",
              fieldValue: "={{ $node.Call_Genome_Builder_WF.json.image_id }}"
            },
            {
              fieldName: "batch_id",
              fieldValue: "={{ $node.Set_Execution_Context.json.batch_id }}"
            }
          ]
        }
      }
    },

    // ===== NODE 10: Call Shopify Publisher Sub-Workflow =====
    {
      name: "Call_Shopify_Publisher_WF",
      type: "n8n-nodes-base.executeWorkflow",
      typeVersion: 1,
      position: [1440, 420],
      parameters: {
        workflowId: "{{ $env.TBK_SHOPIFY_PUBLISHER_WF_ID }}",
        waitForCompletion: true,
        workflowFieldsUi: {
          workflowFields: [
            {
              fieldName: "image_id",
              fieldValue: "={{ $node.Call_SEO_Generator_WF.json.image_id }}"
            },
            {
              fieldName: "genome",
              fieldValue: "={{ JSON.stringify($node.Call_Genome_Builder_WF.json.genome) }}"
            },
            {
              fieldName: "seo_content",
              fieldValue: "={{ JSON.stringify($node.Call_SEO_Generator_WF.json.seo_content) }}"
            },
            {
              fieldName: "batch_id",
              fieldValue: "={{ $node.Set_Execution_Context.json.batch_id }}"
            }
          ]
        }
      }
    },

    // ===== NODE 11: Call Audit Logger Sub-Workflow =====
    {
      name: "Call_Audit_Logger_WF",
      type: "n8n-nodes-base.executeWorkflow",
      typeVersion: 1,
      position: [1680, 420],
      parameters: {
        workflowId: "{{ $env.TBK_AUDIT_LOGGER_WF_ID }}",
        waitForCompletion: false,  // Async logging
        workflowFieldsUi: {
          workflowFields: [
            {
              fieldName: "image_id",
              fieldValue: "={{ $node.Call_Shopify_Publisher_WF.json.image_id }}"
            },
            {
              fieldName: "stage",
              fieldValue: "all"
            },
            {
              fieldName: "results",
              fieldValue: "={{ JSON.stringify($node.Call_Shopify_Publisher_WF.json) }}"
            },
            {
              fieldName: "batch_id",
              fieldValue: "={{ $node.Set_Execution_Context.json.batch_id }}"
            }
          ]
        }
      }
    },

    // ===== NODE 12: Aggregate Results =====
    {
      name: "Aggregate_Results",
      type: "n8n-nodes-base.code",
      typeVersion: 2,
      position: [240, 560],
      parameters: {
        language: "javaScript",
        jsCode: `
const validation = $node.Call_Input_Validation_WF.json;
const vision = $node.Call_Qwen_Vision_WF.json;
const genome = $node.Call_Genome_Builder_WF.json;
const seo = $node.Call_SEO_Generator_WF.json;
const publish = $node.Call_Shopify_Publisher_WF.json;

const determineStatus = (results) => {
  if (results.publish?.publish_status === "success") {
    return "success";
  } else if (results.publish?.publish_status === "failed") {
    return "failed";
  } else {
    return "partial";
  }
};

return {
  batch_id: $node.Set_Execution_Context.json.batch_id,
  execution_id: $node.Set_Execution_Context.json.execution_id,
  status: determineStatus({ publish }),
  results: {
    validation,
    vision,
    genome,
    seo,
    publish
  },
  processed_at: new Date().toISOString(),
  duration_ms: Date.now() - Date.parse($node.Set_Execution_Context.json.timestamp),
  summary: {
    files_validated: validation?.validated?.length || 0,
    files_rejected: validation?.rejected?.length || 0,
    vision_success: vision?.latency_ms ? true : false,
    publish_success: publish?.publish_status === "success",
    errors: [
      ...(validation?.error_log || []),
      ...(vision?.error ? [vision.error] : [])
    ]
  }
};
`
      }
    },

    // ===== NODE 13: PostgreSQL - Update Batch Status =====
    {
      name: "Update_Batch_Status",
      type: "n8n-nodes-base.postgres",
      typeVersion: 2,
      position: [480, 560],
      parameters: {
        operation: "executeQuery",
        query: `UPDATE batches 
          SET status = $1, completed_at = NOW(), 
              processed_count = $2, error_count = $3,
              execution_metadata = $4
          WHERE batch_id = $5
          RETURNING batch_id, status, completed_at;`,
        queryParametersUi: {
          parameters: [
            {
              name: "$1",
              value: "={{ $node.Aggregate_Results.json.status }}"
            },
            {
              name: "$2",
              value: "={{ $node.Aggregate_Results.json.summary.files_validated }}"
            },
            {
              name: "$3",
              value: "={{ $node.Aggregate_Results.json.summary.files_rejected + $node.Aggregate_Results.json.summary.errors.length }}"
            },
            {
              name: "$4",
              value: "={{ JSON.stringify($node.Aggregate_Results.json) }}"
            },
            {
              name: "$5",
              value: "={{ $node.Set_Execution_Context.json.batch_id }}"
            }
          ]
        }
      },
      credentials: {
        postgres: "postgres_tbk_credentials"
      }
    },

    // ===== NODE 14: Slack Notification =====
    {
      name: "Slack_Notification",
      type: "n8n-nodes-base.slack",
      typeVersion: 3,
      position: [720, 560],
      parameters: {
        channel: "#tbk-pipeline-notifications",
        text: "=== Batch Execution Complete ===",
        attachments: [
          {
            title: "Pipeline Execution Summary",
            text: "={{ $node.Aggregate_Results.json.status === 'success' ? '✅ SUCCESS' : '⚠️ ' + $node.Aggregate_Results.json.status.toUpperCase() }}",
            fields: [
              {
                title: "Batch ID",
                value: "={{ $node.Set_Execution_Context.json.batch_id }}",
                short: true
              },
              {
                title: "Status",
                value: "={{ $node.Aggregate_Results.json.status }}",
                short: true
              },
              {
                title: "Execution ID",
                value: "={{ $node.Set_Execution_Context.json.execution_id }}",
                short: true
              },
              {
                title: "Files Processed",
                value: "={{ $node.Aggregate_Results.json.summary.files_validated }}",
                short: true
              },
              {
                title: "Files Rejected",
                value: "={{ $node.Aggregate_Results.json.summary.files_rejected }}",
                short: true
              },
              {
                title: "Duration",
                value: "={{ ($node.Aggregate_Results.json.duration_ms / 1000).toFixed(2) }}s",
                short: true
              },
              {
                title: "Errors",
                value: "={{ $node.Aggregate_Results.json.summary.errors.length }}",
                short: true
              }
            ],
            color: "={{ $node.Aggregate_Results.json.status === 'success' ? 'good' : 'danger' }}"
          }
        ]
      },
      credentials: {
        slackApi: "slack_webhook_credentials"
      }
    },

    // ===== NODE 15: Datadog Metrics =====
    {
      name: "Send_Datadog_Metrics",
      type: "n8n-nodes-base.httpRequest",
      typeVersion: 4,
      position: [960, 560],
      parameters: {
        url: "https://api.datadoghq.com/api/v1/series",
        method: "POST",
        headers: {
          "DD-API-KEY": "={{ $env.DATADOG_API_KEY }}",
          "Content-Type": "application/json"
        },
        body: "={{ JSON.stringify({ series: [ { metric: 'tbk.vision.batch.duration', points: [[Date.now() / 1000, parseInt($node.Aggregate_Results.json.duration_ms)]], tags: ['env:prod', `batch_id:${$node.Set_Execution_Context.json.batch_id}`, `status:${$node.Aggregate_Results.json.status}`] }, { metric: 'tbk.vision.batch.success_rate', points: [[Date.now() / 1000, ($node.Aggregate_Results.json.summary.files_validated / $node.Set_Execution_Context.json.file_count) * 100]], tags: [`batch_id:${$node.Set_Execution_Context.json.batch_id}`] } ] }) }}",
        bodyParametersUi: {
          parameter: []
        },
        authentication: "none"
      },
      onError: "continueRegardlessOfError"
    },

    // ===== NODE 16: Error Handler =====
    {
      name: "Error_Handler",
      type: "n8n-nodes-base.errorTrigger",
      typeVersion: 1,
      position: [1200, 560],
      parameters: {}
    },

    // ===== NODE 17: Error Notification =====
    {
      name: "Error_Slack_Alert",
      type: "n8n-nodes-base.slack",
      typeVersion: 3,
      position: [1440, 560],
      parameters: {
        channel: "#tbk-pipeline-alerts",
        text: "🚨 Pipeline Error",
        attachments: [
          {
            title: "Error Details",
            text: "={{ $json.error.message }}",
            fields: [
              {
                title: "Batch ID",
                value: "={{ $node.Set_Execution_Context.json.batch_id }}"
              },
              {
                title: "Error Type",
                value: "={{ $json.error.name }}"
              }
            ],
            color: "danger"
          }
        ]
      },
      credentials: {
        slackApi: "slack_webhook_credentials"
      }
    },

    // ===== NODE 18: HTTP Response =====
    {
      name: "HTTP_Response",
      type: "n8n-nodes-base.httpResponse",
      typeVersion: 1,
      position: [1680, 560],
      parameters: {
        status: 200,
        responseBody: "={{ JSON.stringify({ success: true, batch_id: $node.Set_Execution_Context.json.batch_id, status: $node.Aggregate_Results.json.status }) }}"
      }
    }
  ],
  
  connections: {
    "Webhook_Trigger": {
      [NodeConnectionType.Main]: [[{ node: "Set_Execution_Context", type: NodeConnectionType.Main, index: 0 }]]
    },
    "Set_Execution_Context": {
      [NodeConnectionType.Main]: [[{ node: "Validate_Input_Schema", type: NodeConnectionType.Main, index: 0 }]]
    },
    "Validate_Input_Schema": {
      [NodeConnectionType.Main]: [[{ node: "Create_Batch_Record", type: NodeConnectionType.Main, index: 0 }]]
    },
    "Create_Batch_Record": {
      [NodeConnectionType.Main]: [[{ node: "Loop_Each_File", type: NodeConnectionType.Main, index: 0 }]]
    },
    "Loop_Each_File": {
      [NodeConnectionType.Main]: [[{ node: "Call_Input_Validation_WF", type: NodeConnectionType.Main, index: 0 }]]
    },
    "Call_Input_Validation_WF": {
      [NodeConnectionType.Main]: [[{ node: "Call_Qwen_Vision_WF", type: NodeConnectionType.Main, index: 0 }]]
    },
    "Call_Qwen_Vision_WF": {
      [NodeConnectionType.Main]: [[{ node: "Call_Genome_Builder_WF", type: NodeConnectionType.Main, index: 0 }]]
    },
    "Call_Genome_Builder_WF": {
      [NodeConnectionType.Main]: [[{ node: "Call_SEO_Generator_WF", type: NodeConnectionType.Main, index: 0 }]]
    },
    "Call_SEO_Generator_WF": {
      [NodeConnectionType.Main]: [[{ node: "Call_Shopify_Publisher_WF", type: NodeConnectionType.Main, index: 0 }]]
    },
    "Call_Shopify_Publisher_WF": {
      [NodeConnectionType.Main]: [
        [{ node: "Call_Audit_Logger_WF", type: NodeConnectionType.Main, index: 0 }],
        [{ node: "Aggregate_Results", type: NodeConnectionType.Main, index: 0 }]
      ]
    },
    "Call_Audit_Logger_WF": {
      [NodeConnectionType.Main]: [[{ node: "Aggregate_Results", type: NodeConnectionType.Main, index: 0 }]]
    },
    "Aggregate_Results": {
      [NodeConnectionType.Main]: [[{ node: "Update_Batch_Status", type: NodeConnectionType.Main, index: 0 }]]
    },
    "Update_Batch_Status": {
      [NodeConnectionType.Main]: [
        [{ node: "Slack_Notification", type: NodeConnectionType.Main, index: 0 }],
        [{ node: "Send_Datadog_Metrics", type: NodeConnectionType.Main, index: 0 }],
        [{ node: "HTTP_Response", type: NodeConnectionType.Main, index: 0 }]
      ]
    },
    "Error_Handler": {
      [NodeConnectionType.Main]: [[{ node: "Error_Slack_Alert", type: NodeConnectionType.Main, index: 0 }]]
    },
    "Error_Slack_Alert": {
      [NodeConnectionType.Main]: [[{ node: "HTTP_Response", type: NodeConnectionType.Main, index: 0 }]]
    }
  },

  active: true,
  settings: {
    executionOrder: "v1",
    saveDataErrorExecution: "all",
    saveDataSuccessExecution: "all",
    errorHandler: "Error_Handler",
    timezone: "UTC"
  },

  staticData: null,
  meta: {
    instanceId: null
  }
};
