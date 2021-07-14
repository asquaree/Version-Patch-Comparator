
importing libraries;

//thi function will return the repository
repository get_repo(address add)
{
    repo=git clone add;
    return repo
}

//this function will return a list of all versions;
vector<version> get_all_versions(repository repo)
{
    vector<version> all_versions;//a list of versions

    int n(number_of_branches)= git branch//number of branches in the repo
    for(int i=0;i<n;i++)
    {
        all_versions.push_back(git --single branch repobranch(i));
    }

    return all_version;
}

//this function will return a list of patches in each version
vector<vector<patch>> get_patches(vector<version> all_versions)
{
    vector<vector<patch>> version_patch; //a list of patches of each version

    for(int i=0;i<all_versions.size();i++)
    {
        vector<patch> patches; //a list of patches
        for(int j=0;j<all_versions[i].size();j++)
        {
            if(all_version[i][j] extension==.patch)
            {
                patches.push_back(all_version[i][j]);
            }
        }
        patches.sort();// sorting the patches name wise
        version_patch.push_back(patches);
    }

    return version_patch;
}

vector<vector<text>> extract_files(repo)
{
    vector<versions> all_versions =get_all_versions(repo);// all the version in repo

    vector<vector<patch>> version_patch = get_patches(all_versions); // a list of all the patches in each version

    vector<vector<text>> consecutive_versions_patch_comparison_files; // a list of patch comparision files of consecutive versions for eg [f10 f11,f11 f12]

    for(int i=1;i<all_versions.size();i++)
    {
        cout<<"comparing version"<<i<<"with"<<i-1;
        vector<text> patch1a_patch1b; // text file consisting of difference between consecutive same patch files

        map<patch,int> patch_frq;

        for(int j=0;j<version_patch[i-1].size();j++)
        {
            patch_frq[version_patch[i-1][j]]++;
        }

        for(int j=0;j<version_patch[i].size();j++)
        {
            text diff_file; //difference file
            if(patch_frq[version_patch[i][j]]>0)
            {
                diff_file=compare_patch(version_patch[i][j],version_patch[i-1][j]) //a text file with + if line or function is more i version and - if line or function is more in i-1 version
                patch_frq[version_patch[i][j]].remove() // removing already compared patch from map
            }
            else
            {
                diff_file=asitis(version_patch[i][j]); // a text file containing all functions and lines with + sign
            }
            patch1a_patch1b.push_back(diff_file);
        }

        consecutive_versions_patch_comparison_files.push_back(patch1a_patch1b);
    }

    return consecutive_versions_patch_comparison_files;

    //[[p1,p2,p3,p4],[p1,p4,p7,p5]]
    //      ^               ^
    //      |               |
    //      f10,f11        f11,f12
}


int main()
{
    repository repo=get_repo(repo address);//repo

    vector<vector<text>> consecutive_versions_each_patch_compared_files = extract_files(repo);

    for(int i=0;i<consecutive_versions_each_patch_compared_files.size();i++)
    {
        cout<<"diff files of f10 and fedora 11"<<"\n";

        for(int j=0;j<consecutive_versions_each_patch_compared_files[i].size();i++)
        {
            cout<<"diff 1(f10 patcha compared with f11 patcha)"<<'\n';
            cout<<consecutive_versions_each_patch_compared_files[i][j]<<"\n";
        }
    }







}
