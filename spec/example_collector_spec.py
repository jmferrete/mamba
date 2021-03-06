# -*- coding: utf-8 -*-

import os
import sys
import inspect

from mamba import example, example_group, loader
from mamba.example_collector import ExampleCollector

from expects import *


def spec_relpath(name):
    return os.path.join('spec', 'fixtures', name)


def spec_abspath(name):
    return os.path.join(os.path.dirname(__file__), 'fixtures', name)


IRRELEVANT_PATH = spec_abspath('without_inner_contexts.py')
PENDING_DECORATOR_PATH = spec_abspath('with_pending_decorator.py')
PENDING_DECORATOR_AS_ROOT_PATH = spec_abspath('with_pending_decorator_as_root.py')
IGNORE_REST_DECORATOR_PATH = spec_abspath('with_ignore_rest_decorator.py')
MULTI_IGNORE_REST_DECORATOR_PATH = spec_abspath('with_multi_ignore_rest_decorator.py')
MULTI_IGNORE_REST_CONTEXTS_DECORATOR_PATH = spec_abspath('with_multi_ignore_rest_contexts_decorator.py')
COMBINED_IGNORE_REST_DECORATOR_PATH = spec_abspath('with_combined_ignore_rest_decorator.py')
WITH_RELATIVE_IMPORT_PATH = spec_abspath('with_relative_import.py')


def _load_module(path):
    example_collector = ExampleCollector([path])
    return list(example_collector.modules())[0]


with description(ExampleCollector) as _:
    with context('when loading from file'):
        with it('loads module from absolute path'):
            module = _load_module(IRRELEVANT_PATH)

            expect(inspect.ismodule(module)).to(be_true)

        with it('loads module from relative path'):
            module = _load_module(spec_relpath('without_inner_contexts.py'))

            expect(inspect.ismodule(module)).to(be_true)

    #FIXME: Mixed responsabilities in test [collect, load]??
    with context('when loading'):
        with it('orders examples by line number'):
            module = _load_module(spec_abspath('without_inner_contexts.py'))

            examples = loader.Loader().load_examples_from(module)

            expect(examples).to(have_length(1))
            expect([example.name for example in examples[0].examples]).to(equal(['it first example', 'it second example', 'it third example']))

        with it('places examples together and groups at the end'):
            module = _load_module(spec_abspath('with_inner_contexts.py'))

            examples = loader.Loader().load_examples_from(module)

            expect(examples).to(have_length(1))
            expect([example.name for example in examples[0].examples]).to(equal(['it first example', 'it second example', 'it third example', '#inner_context']))

    with context('when a pending decorator loaded'):
        with it('mark example as pending'):
            module = _load_module(PENDING_DECORATOR_PATH)

            examples = loader.Loader().load_examples_from(module)

            expect(examples).to(have_length(1))
            expect(examples[0].examples[0]).to(be_a(example.PendingExample))

        with it('marks example group as pending'):
            module = _load_module(PENDING_DECORATOR_PATH)

            examples = loader.Loader().load_examples_from(module)

            expect(examples).to(have_length(1))
            expect(examples[0].examples[1]).to(be_a(example_group.PendingExampleGroup))

    with context('when a pending decorator loaded_as_root'):
        with it('mark inner examples as pending'):
            module = _load_module(PENDING_DECORATOR_AS_ROOT_PATH)

            examples = loader.Loader().load_examples_from(module)

            expect(examples).to(have_length(1))
            examples_in_root = examples[0].examples

            expect(examples_in_root).to(have_length(2))
            expect(examples_in_root[0]).to(be_a(example.PendingExample))
            expect(examples_in_root[1]).to(be_a(example_group.PendingExampleGroup))
            expect(examples_in_root[1].examples[0]).to(be_a(example.PendingExample))

    with context('when loading with relative import'):
        with it('loads module and perform relative import'):
            module = _load_module(WITH_RELATIVE_IMPORT_PATH)

            expect(module).to(have_property('HelperClass'))


    with context('when a ignore rest decorator loaded'):
        with it('ignore rest of examples like pending examples'):
            module = _load_module(IGNORE_REST_DECORATOR_PATH)

            examples = loader.Loader().load_examples_from(module)

            expect(examples).to(have_length(1))
            expect(examples[0].examples[0].examples[0]).to(be_a(example.PendingExample))
            expect(examples[0].examples[0].examples[1]).to(be_a(example.Example))
            expect(examples[0].examples[0].examples[2]).to(be_a(example.PendingExample))
            expect(examples[0].examples[0].examples[3]).to(be_a(example.PendingExample))


    with context('when two ignore rest decorator loaded'):
        with it('only the last ignore rest is executed'):
            module = _load_module(MULTI_IGNORE_REST_DECORATOR_PATH)

            examples = loader.Loader().load_examples_from(module)

            expect(examples).to(have_length(1))
            expect(examples[0].examples[0].examples[0]).to(be_a(example.PendingExample))
            expect(examples[0].examples[0].examples[1]).to(be_a(example.PendingExample))
            expect(examples[0].examples[0].examples[2]).to(be_a(example.PendingExample))
            expect(examples[0].examples[0].examples[3]).to(be_a(example.PendingExample))
            expect(examples[0].examples[0].examples[4]).to(be_a(example.Example))


    with context('when a ignore rest contexts loaded'):
        with it('ignore rest of contexts like pending contexts'):
            module = _load_module(MULTI_IGNORE_REST_CONTEXTS_DECORATOR_PATH)

            examples = loader.Loader().load_examples_from(module)

            expect(examples).to(have_length(1))
            expect(examples[0].examples[0]).to(be_a(example_group.PendingExampleGroup))
            expect(examples[0].examples[1]).to(be_a(example_group.ExampleGroup))
            expect(examples[0].examples[2]).to(be_a(example_group.PendingExampleGroup))


    with context('when there are ignore rest in various contexts and examples loaded'):
        with it('only the last ignore rest example is executed in the last context marked as ignore rest'):
            module = _load_module(COMBINED_IGNORE_REST_DECORATOR_PATH)

            examples = loader.Loader().load_examples_from(module)

            expect(examples).to(have_length(1))
            expect(examples[0].examples[0].examples[0]).to(be_a(example.PendingExample))
            expect(examples[0].examples[1].examples[0]).to(be_a(example.PendingExample))
            expect(examples[0].examples[1].examples[1]).to(be_a(example.PendingExample))
            expect(examples[0].examples[1].examples[2]).to(be_a(example.PendingExample))
            expect(examples[0].examples[1].examples[3]).to(be_a(example.PendingExample))
            expect(examples[0].examples[1].examples[4]).to(be_a(example.Example))
            expect(examples[0].examples[1].examples[5]).to(be_a(example.PendingExample))