from dataclasses import replace
from typing import Union

from adaptix import Mediator, CannotProvide
from adaptix._internal.common import Coercer
from adaptix._internal.conversion.coercer_provider import StrippedTypeCoercerProvider
from adaptix._internal.conversion.request_cls import CoercerRequest
from adaptix._internal.type_tools import BaseNormType


class OptionalCoercerProvider(StrippedTypeCoercerProvider):
    def _provide_coercer_stripped_types(
        self,
        mediator: Mediator,
        request: CoercerRequest,
        stripped_src: BaseNormType,
        stripped_dst: BaseNormType,
    ) -> Coercer:
        if not (self._is_optional(stripped_dst) and self._is_optional(stripped_src)):
            raise CannotProvide

        not_none_src = self._get_not_none(stripped_src)
        not_none_dst = self._get_not_none(stripped_dst)
        not_none_request = replace(
            request,
            src=request.src.replace_last(replace(request.src.last, type=not_none_src)),
            dst=request.dst.replace_last(replace(request.dst.last, type=not_none_dst)),
        )
        not_none_coercer = mediator.delegating_provide(not_none_request)

        def optional_coercer(data):
            if data is None:
                return None
            return not_none_coercer(data)

        return optional_coercer

    def _is_optional(self, norm: BaseNormType) -> bool:
        return norm.origin == Union and None in [case.origin for case in norm.args]

    def _get_not_none(self, norm: BaseNormType) -> BaseNormType:
        return next(case.origin for case in norm.args if case.origin is not None)
