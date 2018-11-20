# Copyright 2018 The Shabda Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
A class that executes training, evaluation, prediction, export of estimators.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf

from vitaflow.utils.dtypes import maybe_hparams_to_dict

# pylint: disable=too-many-instance-attributes, too-many-arguments

__all__ = [
    "Executor"
]

class Executor(object):
    """Class that executes training, evaluation, prediction, export, and other
    actions of :tf_main:`tf.estimator.Estimator <estimator/Estimator>`.

    Args:
        model: An instance of a subclass of
            :class:`~shabda.models.model_base.ModelBase`.
        data_hparams: A `dict` or an instance of :class:`~shabda.hparams.HParams`
            containing the hyperparameters of data. It must contain `train`
            and/or `eval` fields for relevant processes. For example, for
            :meth:`train_and_evaluate`, both fields are required.
        config: An instance of
            :tf_main:`tf.estimator.RunConfig <estimator/RunConfig>`, used as
            the :attr:`config` argument of
            :tf_main:`Estimator <estimator/Estimator#__init__>`.
        model_hparams (optional): A `dict` or an instance of
            :class:`~shabda.hparams.HParams` containing the hyperparameters of
            the model. If `None`, uses :attr:`model.hparams`. Used as
            the :attr:`params` argument of
            :tf_main:`Estimator <estimator/Estimator#__init__>`.
        train_hooks (optional): Iterable of :tf_main:`tf.train.SessionRunHook <train/SessionRunHook>`
            objects to run during training.
        eval_hooks (optional): Iterable of :tf_main:`tf.train.SessionRunHook <train/SessionRunHook>`
            objects to run during evaluation.
        session_config (optional): An instance of
            :tf_main:`tf.ConfigProto <ConfigProto>`, used as the :attr:`config`
            argument of :tf_main:`tf session <Session>`.

    Example:

        .. code-block:: python

            TODO

    See `bin/train.py` for the usage in detail.
    """

    def __init__(self,
                 model,
                 data_iterator,
                 config,
                 model_hparams=None,
                 train_hooks=None,
                 eval_hooks=None,
                 session_config=None):
        self._model = model
        self._config = config
        self._data_iterator = data_iterator
        self._train_hooks = train_hooks
        self._eval_hooks = eval_hooks
        self._session_config = session_config

        if model_hparams is None:
            model_hparams = model.hparams
        self._model_hparams = maybe_hparams_to_dict(model_hparams)

        self._estimator = tf.estimator.Estimator(
            model_fn=self._model, config=config, params=self._model_hparams)

    def _get_train_spec(self, max_steps=None):
        input_fn = self._data_iterator.train_input_fn()
        # Estimators expect an input_fn to take no arguments.
        # To work around this restriction, we use lambda to capture the arguments and provide the expected interface.
        return tf.estimator.TrainSpec(
            input_fn=lambda:input_fn,
            max_steps=max_steps,
            hooks=self._train_hooks)

    def _get_eval_spec(self, steps):
        input_fn = self._data_iterator.val_input_fn()
        return tf.estimator.EvalSpec(
            input_fn=lambda:input_fn,
            steps=steps,
            hooks=self._eval_hooks)

    def train(self, max_steps=None):
        """Trains the model. See :tf_main:`tf.estimator.Estimator.train
        <estimator/Estimator#train>` for more details.

        Args:
            max_steps (int, optional): Total number of steps for which
                to train model. If `None`, train forever or until the train
                data generates the OutOfRange exception. If OutOfRange occurs
                in the middle, training stops before :attr:`max_steps` steps.
        """
        train_spec = self._get_train_spec(max_steps=max_steps) #TODO
        self._estimator.train(
            input_fn=lambda:self._data_iterator.train_input_fn(), #TODO
            hooks=train_spec.hooks,
            max_steps=train_spec.max_steps)

    def evaluate(self, steps=None, checkpoint_path=None):
        """Evaluates the model. See :tf_main:`tf.estimator.Estimator.evaluate
        <estimator/Estimator#evaluate>` for more details.

        Args:
            steps (int, optional): Number of steps for which to evaluate
                model. If `None`, evaluates until the eval data raises an
                OutOfRange exception.
            checkpoint_path (str, optional): Path of a specific checkpoint to
                evaluate. If `None`, the the latest checkpoint in
                :attr:`config.model_dir` is used. If there are no checkpoints
                in :attr:`model_dir`, evaluation is run with newly initialized
                variables instead of restored from checkpoint.
        """
        eval_spec = self._get_eval_spec(steps=steps) #TODO
        self._estimator.evaluate(
            input_fn=lambda:self._data_iterator.val_input_fn(),
            steps=eval_spec.steps,
            hooks=eval_spec.hooks,
            checkpoint_path=checkpoint_path)

    def train_and_evaluate(self, max_train_steps=None, eval_steps=None):
        """Trains and evaluates the model. See
        :tf_main:`tf.estimator.train_and_evaluate
        <estimator/train_and_evaluate>` for more details.

        Args:
            max_train_steps (int, optional): Total number of steps for which
                to train model. If `None`, train forever or until the train
                data generates the OutOfRange exception. If OutOfRange occurs
                in the middle, training stops before :attr:`max_steps` steps.
            eval_steps (int, optional): Number of steps for which to evaluate
                model. If `None`, evaluates until the eval data raises an
                OutOfRange exception.
        """
        train_spec = self._get_train_spec(max_steps=max_train_steps)
        eval_spec = self._get_eval_spec(steps=eval_steps)
        tf.estimator.train_and_evaluate(self._estimator, train_spec, eval_spec)

