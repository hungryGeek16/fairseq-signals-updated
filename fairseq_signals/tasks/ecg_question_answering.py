from dataclasses import dataclass
import logging
import os

from dataclasses import dataclass, field
from typing import Optional
from omegaconf import MISSING

from fairseq_signals.data import JsonECGQADataset
from fairseq_signals.dataclass import Dataclass
from fairseq_signals.tasks.ecg_text_pretaining import ECGTextPretrainingConfig, ECGTextPretrainingTask

from . import register_task

logger = logging.getLogger(__name__)

@dataclass
class ECGQuestionAnsweringConfig(ECGTextPretrainingConfig):
    json_dataset: bool = field(
        default=True,
        metadata={
            'help': 'if true, load json dataset (default)'
        }
    )

@register_task('ecg_question_answering', dataclass=ECGQuestionAnsweringConfig)
class ECGQuestionAnsweringTask(ECGTextPretrainingTask):
    cfg: ECGQuestionAnsweringConfig
    
    def __init__(self, cfg: ECGQuestionAnsweringConfig):
        super().__init__(cfg)

    @classmethod
    def setup_task(cls, cfg: ECGQuestionAnsweringConfig, **kwargs):
        """Setup the task
        
        Args:
            cfg (ECGDiagnosisConfig): configuration of this task
        """
        return cls(cfg)

    def load_dataset(self, split: str, task_cfg: Dataclass=None, **kwargs):
        data_path = self.cfg.data
        task_cfg = task_cfg or self.cfg
        
        if getattr(task_cfg, 'json_dataset', True):
            json_path = os.path.join(data_path, '{}.json'.format(split))
            self.datasets[split] = JsonECGQADataset(
                json_path,
                pad_token_id=task_cfg.pad_token,
                sep_token_id=task_cfg.sep_token,
                pad=task_cfg.enable_padding,
                sample_rate=task_cfg.get('sample_rate', self.cfg.sample_rate),
                max_sample_size=self.cfg.max_sample_size,
                min_sample_size=self.cfg.min_sample_size,
                max_text_size=self.cfg.max_text_size,
                min_text_size=self.cfg.min_text_size,
                normalize=task_cfg.normalize,
                training=True if 'train' in split else False,
            )
        else:
            #TODO should load pairwise dataset
            raise NotImplementedError()