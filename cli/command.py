"""
Command line interface driver for snakemake workflows
"""
import argparse
import os.path
import snakemake
import sys
import pprint
import json

from . import _program


thisdir = os.path.abspath(os.path.dirname(__file__))
parentdir = os.path.join(thisdir,'..')

def main(sysargs = sys.argv[1:]):

    parser = argparse.ArgumentParser(prog = _program, description='bananas: run snakemake workflows', usage='''bananas <workflow> <parameters> [<target>]

bananas: run snakemake workflows, using the given workflow name & parameters file.

''')

    parser.add_argument('workflowfile')
    parser.add_argument('paramsfile')
    parser.add_argument('-n', '--dry-run', action='store_true')
    parser.add_argument('-f', '--force', action='store_true')
    args = parser.parse_args(sysargs)

    # first, find the Snakefile
    snakefile_this      = os.path.join(thisdir,"Snakefile")
    snakefile_parent    = os.path.join(parentdir,"Snakefile")
    if os.path.exists(snakefile_this):
        snakefile = snakefile_this
    elif os.path.exists(snakefile_parent):
        snakefile = snakefile_parent
    else:
        msg = 'Error: cannot find Snakefile at any of the following locations:\n'
        msg += '{}\n'.format(snakefile_this)
        msg += '{}\n'.format(snakefile_parent)
        sys.stderr.write(msg)
        sys.exit(-1)

    # next, find the workflow config file
    workflowfile = None
    if os.path.exists(args.workflowfile) and not os.path.isdir(args.workflowfile):
        workflowfile = args.workflowfile
    else:
        for suffix in ('', '.json'):
            tryfile = os.path.join(thisdir, args.workflowfile + suffix)
            if os.path.exists(tryfile) and not os.path.isdir(tryfile):
                sys.stderr.write('Found workflowfile at {}\n'.format(tryfile))
                workflowfile = tryfile
                break

    if not workflowfile:
        sys.stderr.write('Error: cannot find workflowfile {}\n'.format(args.workflowfile))
        sys.exit(-1)

    # next, find the workflow params file
    paramsfile = None
    if os.path.exists(args.paramsfile) and not os.path.isdir(args.paramsfile):
        paramsfile = args.paramsfile
    else:
        for suffix in ('', '.json'):
            tryfile = os.path.join(thisdir, args.paramsfile + suffix)
            if os.path.exists(tryfile) and not os.path.isdir(tryfile):
                sys.stderr.write('Found paramsfile at {}\n'.format(tryfile))
                paramsfile = tryfile
                break

    if not paramsfile:
        sys.stderr.write('Error: cannot find paramsfile {}\n'.format(args.paramsfile))
        sys.exit(-1)

    with open(workflowfile, 'rt') as fp:
        workflow_info = json.load(fp)

    target = workflow_info['workflow_target']
    config = dict()

    print('--------')
    print('details!')
    print('\tsnakefile: {}'.format(snakefile))
    print('\tconfig: {}'.format(workflowfile))
    print('\tparams: {}'.format(paramsfile))
    print('\ttarget: {}'.format(target))
    print('--------')

    # run bananas!!
    status = snakemake.snakemake(snakefile, configfile=paramsfile,
                                 targets=[target], printshellcmds=True,
                                 dryrun=args.dry_run, forceall=args.force,
                                 config=config)

    if status: # translate "success" into shell exit code of 0
       return 0
    return 1


if __name__ == '__main__':
    main()

