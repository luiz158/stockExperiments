# -*- coding: utf-8 -*-


from instances import data_engine


@data_engine.for_synched(data_engine.select('RAW'),
                         data_engine.select('RAW_NORMALIZATION_FACTOR'))
def _factory(raw_reference, normalization_reference):

    @data_engine.datasource('NORMALIZED:%s' % (raw_reference),
                            dependencies=[raw_reference, normalization_reference],
                            frequency='B',
                            tags=['NORMALIZED', 'STOCK_TICKS'])
    class Normalized(object):
        def evaluate(self, context, symbol, start=None, end=None):
            df_raw = context.dependencies(raw_reference)
            df_factor = context.dependencies(normalization_reference)
            return (df_raw * df_factor).dropna()
