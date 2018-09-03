# 2. Move to ClangFormat 5

Date: 2018-06-26

## Status

Accepted

## Context

Current version of clang-format is aging an becoming unavailable.

## Decision

We will move to clang-format 5 and not the bleeding edge version. Visual Studio 2017 will ship with clang-format 5 so it makes sense to standardize
on this version across the project.

## Consequences

A full reformat of the code base will be required.
