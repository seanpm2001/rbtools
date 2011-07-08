from datetime import datetime
    def __init__(self, url, body='', headers={}, method="PUT"):
class ClearCaseRepositoryInfo(RepositoryInfo):
    """
    A representation of a ClearCase source code repository. This version knows
    how to find a matching repository on the server even if the URLs differ.
    """

    def __init__(self, path, base_path, vobstag, supports_parent_diffs=False):
        RepositoryInfo.__init__(self, path, base_path,
                                supports_parent_diffs=supports_parent_diffs)
        self.vobstag = vobstag

    def find_server_repository_info(self, server):
        """
        The point of this function is to find a repository on the server that
        matches self, even if the paths aren't the same. (For example, if self
        uses an 'http' path, but the server uses a 'file' path for the same
        repository.) It does this by comparing VOB's name. If the
        repositories use the same path, you'll get back self, otherwise you'll
        get a different ClearCaseRepositoryInfo object (with a different path).
        """

        # Find VOB's family uuid based on VOB's tag
        uuid = self._get_vobs_uuid(self.vobstag)
        debug("Repositorie's %s uuid is %r" % (self.vobstag, uuid))

        repositories = server.get_repositories()
        for repository in repositories:
            if repository['tool'] != 'ClearCase':
                continue

            info = self._get_repository_info(server, repository)

            if not info or uuid != info['uuid']:
                continue

            debug('Matching repository uuid:%s with path:%s' %(uuid,
                  info['repopath']))
            return ClearCaseRepositoryInfo(info['repopath'],
                    info['repopath'], uuid)

        # We didn't found uuid but if version is >= 1.5.3
        # we can try to use VOB's name hoping it is better
        # than current VOB's path.
        if server.rb_version >= '1.5.3':
            self.path = cpath.split(self.vobstag)[1]

        # We didn't find a matching repository on the server.
        # We'll just return self and hope for the best.
        return self

    def _get_vobs_uuid(self, vobstag):
        """Return family uuid of VOB."""

        property_lines = execute(["cleartool", "lsvob", "-long", vobstag],
                                 split_lines=True)
        for line  in property_lines:
            if line.startswith('Vob family uuid:'):
                return  line.split(' ')[-1].rstrip()

    def _get_repository_info(self, server, repository):
        try:
            return server.get_repository_info(repository['id'])
        except APIError, e:
            # If the server couldn't fetch the repository info, it will return
            # code 210. Ignore those.
            # Other more serious errors should still be raised, though.
            if e.error_code == 210:
                return None

            raise e

        self.password_mgr.rb_user = options.http_username
        self.password_mgr.rb_pass = options.http_password
        self._lasturl = ""
        if self._lasturl != args[0]:
            self._retried = False

        self._lasturl = args[0]

            self.retried = 0
            self.rb_version = rsp['info']['product']['package_version']

            if parse_version(self.rb_version) >= parse_version('1.5.2'):
            if e.http_status not in (401, 404):
                #
                # However in some versions it wants you to be logged in
                # and returns a 401 from the application after you've
                # done your http basic auth
        repository = options.repository_url \
                     or self.get_configured_repository() \
                     or self.info.path
            self.api_post(
            self.api_put(review_request['links']['self']['href'], {
        debug('HTTP DELETing %s' % url)
            r = HTTPRequest(url, method='DELETE')
        return (None, None)
        i = repository_path.rfind(":")
        return (self.do_diff(revs + args), None)
    viewtype = None
        """Returns information on the Clear Case repository.

        This will first check if the cleartool command is
        installed and in the path, and post-review was run
        from inside of the view.
        """
        viewname = execute(["cleartool", "pwv", "-short"]).strip()
        if viewname.startswith('** NONE'):
        # Now that we know it's ClearCase, make sure we have GNU diff installed,
        # and error out if we don't.
        check_gnu_diff()

        property_lines = execute(["cleartool", "lsview", "-full", "-properties",
                                  "-cview"], split_lines=True)
        for line in property_lines:
            properties = line.split(' ')
            if properties[0] == 'Properties:':
                # Determine the view type and check if it's supported.
                #
                # Specifically check if webview was listed in properties
                # because webview types also list the 'snapshot'
                # entry in properties.
                if 'webview' in properties:
                    die("Webviews are not supported. You can use post-review"
                        " only in dynamic or snapshot view.")
                if 'dynamic' in properties:
                    self.viewtype = 'dynamic'
                else:
                    self.viewtype = 'snapshot'

                break

        # Find current VOB's tag
        vobstag = execute(["cleartool", "describe", "-short", "vob:."],
                            ignore_errors=True).strip()
        if "Error: " in vobstag:
            die("To generate diff run post-review inside vob.")

        # From current working directory cut path to VOB.
        # VOB's tag contain backslash character before VOB's name.
        # I hope that first character of VOB's tag like '\new_proj'
        # won't be treat as new line character but two separate:
        # backslash and letter 'n'
        cwd = os.getcwd()
        base_path = cwd[:cwd.find(vobstag) + len(vobstag)]

        return ClearCaseRepositoryInfo(path=base_path,
                              base_path=base_path,
                              vobstag=vobstag,
    def check_options(self):
        if ((options.revision_range or options.tracking)
            and self.viewtype != "dynamic"):
            die("To generate diff using parent branch or by passing revision "
                "ranges, you must use a dynamic view.")

    def _determine_version(self, version_path):
        """Determine numeric version of revision.

        CHECKEDOUT is marked as infinity to be treated
        always as highest possible version of file.
        CHECKEDOUT, in ClearCase, is something like HEAD.
        """
        branch, number = cpath.split(version_path)
        if number == 'CHECKEDOUT':
            return float('inf')
        return int(number)

    def _construct_extended_path(self, path, version):
        """Combine extended_path from path and version.

        CHECKEDOUT must be removed becasue this one version
        doesn't exists in MVFS (ClearCase dynamic view file
        system). Only way to get content of checked out file
        is to use filename only."""
        if not version or version.endswith('CHECKEDOUT'):
            return path
        return "%s@@%s" % (path, version)
    def _sanitize_branch_changeset(self, changeset):
        """Return changeset containing non-binary, branched file versions.
        Changeset contain only first and last version of file made on branch.
        """
        changelist = {}
        for path, previous, current in changeset:
            version_number = self._determine_version(current)
            if path not in changelist:
                changelist[path] = {
                    'highest': version_number,
                    'current': current,
                    'previous': previous
                }
            if version_number == 0:
                # Previous version of 0 version on branch is base
                changelist[path]['previous'] = previous
            elif version_number > changelist[path]['highest']:
                changelist[path]['highest'] = version_number
                changelist[path]['current'] = current

        # Convert to list
        changeranges = []
        for path, version in changelist.iteritems():
            changeranges.append(
                (self._construct_extended_path(path, version['previous']),
                 self._construct_extended_path(path, version['current']))
            )

        return changeranges

    def _sanitize_checkedout_changeset(self, changeset):
        """Return changeset containing non-binary, checkdout file versions."""

        changeranges = []
        for path, previous, current in changeset:
            version_number = self._determine_version(current)
            changeranges.append(
                (self._construct_extended_path(path, previous),
                self._construct_extended_path(path, current))
            )

        return changeranges

    def _directory_content(self, path):
        """Return directory content ready for saving to tempfile."""

        return ''.join([
            '%s\n' % s
            for s in sorted(os.listdir(path))
        ])

    def _construct_changeset(self, output):
        return [
            info.split('\t')
            for info in output.strip().split('\n')
        ]

    def get_checkedout_changeset(self):
        """Return information about the checked out changeset.

        This function returns: kind of element, path to file,
        previews and current file version.
        """
        changeset = []
        # We ignore return code 1 in order to
        # omit files that Clear Case can't read.
        output = execute([
            "cleartool",
            "lscheckout",
            "-all",
            "-cview",
            "-me",
            "-fmt",
            r"%En\t%PVn\t%Vn\n"],
            extra_ignore_errors=(1,),
            with_errors=False)

        if output:
            changeset = self._construct_changeset(output)

        return self._sanitize_checkedout_changeset(changeset)

    def get_branch_changeset(self, branch):
        """Returns information about the versions changed on a branch.

        This takes into account the changes on the branch owned by the
        current user in all vobs of the current view.
        """
        changeset = []

        # We ignore return code 1 in order to
        # omit files that Clear Case can't read.
        if sys.platform.startswith('win'):
            CLEARCASE_XPN = '%CLEARCASE_XPN%'
        else:
            CLEARCASE_XPN = '$CLEARCASE_XPN'

        output = execute([
            "cleartool",
            "find",
            "-all",
            "-version",
            "brtype(%s)" % branch,
            "-exec",
            'cleartool descr -fmt ' \
            r'"%En\t%PVn\t%Vn\n" ' \
            + CLEARCASE_XPN],
            extra_ignore_errors=(1,),
            with_errors=False)

        if output:
            changeset = self._construct_changeset(output)

        return self._sanitize_branch_changeset(changeset)
        """Performs a diff of the specified file and its previous version."""
        if options.tracking:
            changeset = self.get_branch_changeset(options.tracking)
        else:
            changeset = self.get_checkedout_changeset()

        return self.do_diff(changeset)
        """Performs a diff between passed revisions or branch."""

        # Convert revision range to list of:
        # (previous version, current version) tuples
        revision_range = revision_range.split(';')
        changeset = zip(revision_range[0::2], revision_range[1::2])

        return (self.do_diff(changeset)[0], None)

    def diff_files(self, old_file, new_file):
        """Return unified diff for file.

        Most effective and reliable way is use gnu diff.
        diff_cmd = ["diff", "-uN", old_file, new_file]
        dl = execute(diff_cmd, extra_ignore_errors=(1,2),
                     translate_newlines=False)

        # If the input file has ^M characters at end of line, lets ignore them.
        dl = dl.replace('\r\r\n', '\r\n')
        dl = dl.splitlines(True)

        # Special handling for the output of the diff tool on binary files:
        #     diff outputs "Files a and b differ"
        # and the code below expects the output to start with
        #     "Binary files "
        if (len(dl) == 1 and
            dl[0].startswith('Files %s and %s differ' % (old_file, new_file))):
            dl = ['Binary files %s and %s differ\n' % (old_file, new_file)]

        # We need oids of files to translate them to paths on reviewboard repository
        old_oid = execute(["cleartool", "describe", "-fmt", "%On", old_file])
        new_oid = execute(["cleartool", "describe", "-fmt", "%On", new_file])

        if dl == [] or dl[0].startswith("Binary files "):
            if dl == []:
                dl = ["File %s in your changeset is unmodified\n" % new_file]

            dl.insert(0, "==== %s %s ====\n" % (old_oid, new_oid))
            dl.append('\n')
        else:
            dl.insert(2, "==== %s %s ====\n" % (old_oid, new_oid))

        return dl

    def diff_directories(self, old_dir, new_dir):
        """Return uniffied diff between two directories content.

        Function save two version's content of directory to temp
        files and treate them as casual diff between two files.
        old_content = self._directory_content(old_dir)
        new_content = self._directory_content(new_dir)
        old_tmp = make_tempfile(content=old_content)
        new_tmp = make_tempfile(content=new_content)

        diff_cmd = ["diff", "-uN", old_tmp, new_tmp]
        dl = execute(diff_cmd,
                     extra_ignore_errors=(1,2),
                     translate_newlines=False,
                     split_lines=True)

        # Replacing temporary filenames to
        # real directory names and add ids
        if dl:
            dl[0] = dl[0].replace(old_tmp, old_dir)
            dl[1] = dl[1].replace(new_tmp, new_dir)
            old_oid = execute(["cleartool", "describe", "-fmt", "%On", old_dir])
            new_oid = execute(["cleartool", "describe", "-fmt", "%On", new_dir])
            dl.insert(2, "==== %s %s ====\n" % (old_oid, new_oid))

        return dl

    def do_diff(self, changeset):
        """Generates a unified diff for all files in the changeset."""

        diff = []
        for old_file, new_file in changeset:
            dl = []
            if cpath.isdir(new_file):
                dl = self.diff_directories(old_file, new_file)
            elif cpath.exists(new_file):
                dl = self.diff_files(old_file, new_file)
            else:
                debug("File %s does not exist or access is denied." % new_file)
                continue

            if dl:
                diff.append(''.join(dl))

        return (''.join(diff), None)
    # Match the diff control lines generated by 'svn diff'.
    DIFF_ORIG_FILE_LINE_RE = re.compile(r'^---\s+.*\s+\(.*\)')
    DIFF_NEW_FILE_LINE_RE = re.compile(r'^\+\+\+\s+.*\s+\(.*\)')

    def diff_changelist(self, changelist):
        """
        Performs a diff for a local changelist.
        """
        return (self.do_diff(["svn", "diff", "--changelist", changelist]),
                None)

            return (self.do_diff(["svn", "diff", "--diff-cmd=diff", old_url,
                                  new_url] + files,
                                 repository_info), None)
            return (self.do_diff(["svn", "diff", "--diff-cmd=diff", "-r",
                                  revision_range],
                                 repository_info), None)
            if self.DIFF_ORIG_FILE_LINE_RE.match(line):
            if self.DIFF_NEW_FILE_LINE_RE.match(line):
            if (self.DIFF_NEW_FILE_LINE_RE.match(line)
                or self.DIFF_ORIG_FILE_LINE_RE.match(line)
                or line.startswith('Index: ')):
                return None
        if options.guess_summary and not options.summary:
            options.summary = self.extract_summary(top_rev).rstrip("\n")

        if options.guess_description and not options.description:
            options.description = self.extract_description(bottom_rev, top_rev)

        return (execute(["hg", "diff", "-r", r1, "-r", r2],
                        env=self._hg_env), None)
    def __init__(self):
        SCMClient.__init__(self)
        # Store the 'correct' way to invoke git, just plain old 'git' by default
        self.git = 'git'

            # CreateProcess (launched via subprocess, used by check_install)
            # does not automatically append .cmd for things it finds in PATH.
            # If we're on Windows, and this works, save it for further use.
            if sys.platform.startswith('win') and check_install('git.cmd --help'):
                self.git = 'git.cmd'
            else:
                return None
        git_dir = execute([self.git, "rev-parse", "--git-dir"],
                          ignore_errors=True).rstrip("\n")
        self.bare = execute([self.git, "config", "core.bare"]).strip() == 'true'
        if not self.bare:
            os.chdir(os.path.dirname(os.path.abspath(git_dir)))
        self.head_ref = execute([self.git, 'symbolic-ref', '-q', 'HEAD']).strip()
            data = execute([self.git, "svn", "info"], ignore_errors=True)

                        # Get SVN tracking branch
                        if options.parent_branch:
                            self.upstream_branch = options.parent_branch
                        else:
                            data = execute([self.git, "svn", "rebase", "-n"],
                                           ignore_errors=True)
                            m = re.search(r'^Remote Branch:\s*(.+)$', data, re.M)

                            if m:
                                self.upstream_branch = m.group(1)
                            else:
                                sys.stderr.write('Failed to determine SVN tracking '
                                                 'branch. Defaulting to "master"\n')
                                self.upstream_branch = 'master'
                version = execute([self.git, "svn", "--version"],
                svn_remote = execute([self.git, "config", "--get",
        merge = execute([self.git, 'config', '--get',
        remote = execute([self.git, 'config', '--get',
        url = None
        if options.repository_url:
            url = options.repository_url
        else:
            self.upstream_branch, origin_url = \
                self.get_origin(self.upstream_branch, True)
            if not origin_url or origin_url.startswith("fatal:"):
                self.upstream_branch, origin_url = self.get_origin()
            url = origin_url.rstrip('/')

        # Central bare repositories don't have origin URLs.
        # We return git_dir instead and hope for the best.

        if not url:
            url = os.path.abspath(git_dir)

            # There is no remote, so skip this part of upstream_branch.
            self.upstream_branch = self.upstream_branch.split('/')[-1]
        origin_url = execute([self.git, "config", "--get",
                              "remote.%s.url" % upstream_remote],
                              ignore_errors=True).rstrip("\n")
        return (upstream_branch, origin_url)
        url = execute([self.git, "config", "--get", "reviewboard.url"],
        self.merge_base = execute([self.git, "merge-base", self.upstream_branch,
            options.summary = execute([self.git, "log", "--pretty=format:%s",
                [self.git, "log", "--pretty=format:%s%n%n%b",
        if commit:
            rev_range = "%s..%s" % (ancestor, commit)
        else:
            rev_range = ancestor
            diff_lines = execute([self.git, "diff", "--no-color", "--no-prefix",
            return execute([self.git, "diff", "--no-color", "--full-index",
        rev = execute([self.git, "svn", "find-rev", parent_branch]).strip()

        # Make a parent diff to the first of the revisions so that we
        # never end up with broken patches:
        self.merge_base = execute([self.git, "merge-base", self.upstream_branch,
                                   self.head_ref]).strip()


            # Check if parent contains the first revision and make a
            # parent diff if not:
            pdiff_required = execute([self.git, "branch", "-r",
                                      "--contains", revision_range])
            parent_diff_lines = None

            if not pdiff_required:
                parent_diff_lines = self.make_diff(self.merge_base, revision_range)

                    [self.git, "log", "--pretty=format:%s", revision_range + ".."],
                    [self.git, "log", "--pretty=format:%s%n%n%b", revision_range + ".."],
            return (self.make_diff(revision_range), parent_diff_lines)
            # Check if parent contains the first revision and make a
            # parent diff if not:
            pdiff_required = execute([self.git, "branch", "-r",
                                      "--contains", r1])
            parent_diff_lines = None

            if not pdiff_required:
                parent_diff_lines = self.make_diff(self.merge_base, r1)
                    [self.git, "log", "--pretty=format:%s", "%s..%s" % (r1, r2)],
                    [self.git, "log", "--pretty=format:%s%n%n%b", "%s..%s" % (r1, r2)],
            return (self.make_diff(r1, r2), parent_diff_lines)
        return (self.branch_diff(revision_range), None)
def make_tempfile(content=None):
    if content:
        os.write(fd, content)
        subprocess.Popen(command.split(' '),
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
            extra_ignore_errors=(), translate_newlines=True, with_errors=True):
    if with_errors:
        errors_output = subprocess.STDOUT
    else:
        errors_output = subprocess.PIPE

                             stderr=errors_output,
                             stderr=errors_output,
    parser.add_option('--svn-changelist', dest='svn_changelist', default=None,
                      help='generate the diff for review based on a local SVN '
                           'changelist')
                           "paths outside the view). For git, this specifies"
                           "the origin url of the current repository, "
                           "overriding the origin url supplied by the git client.")
    parser.add_option('--http-username',
                      dest='http_username', default=None, metavar='USERNAME',
                      help='username for HTTP Basic authentication')
    parser.add_option('--http-password',
                      dest='http_password', default=None, metavar='PASSWORD',
                      help='password for HTTP Basic authentication')
    server.check_api_version()
        diff, parent_diff = tool.diff_between_revisions(options.revision_range, args,
                                                        repository_info)
    elif options.svn_changelist:
        diff, parent_diff = tool.diff_changelist(options.svn_changelist)
        # NOTE: In Review Board 1.5.2 through 1.5.3.1, the changenum support
        #       is broken, so we have to force the deprecated API.
        if (parse_version(server.rb_version) >= parse_version('1.5.2') and
            parse_version(server.rb_version) <= parse_version('1.5.3.1')):
            debug('Using changenums on Review Board %s, which is broken. '
                  'Falling back to the deprecated 1.0 API' % server.rb_version)
            server.deprecated_api = True
